# Review — DESK_SCREENS PR 1a (#116, `feat/desk-visits`): one independent reviewer, read-only

You are an **independent code reviewer** of one pull request in the Git repository at
`C:\dev\masaha\app-design`. Two reviewers run this same file at the same time, separately (Codex and
OpenCode); **do not read the other's report**. This file is self-contained: every command, file and question is
written here. You did not write the code; another agent did. **Trust nothing you have not seen in the code.**

**Your report file** (write only this file, nothing else anywhere):
- if you are **Codex**: `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\6_REVIEW_PR1A_CODEX.md`
- if you are **OpenCode** (or any other agent): `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\6_REVIEW_PR1A_OPENCODE.md`

Write the report **as you go** (a section after each part of §4), so nothing is lost if you stop early.

## 0. What the PR is

Masaha is a bilingual (Arabic right-to-left / English) web platform for coworking spaces. This PR builds, in
the web app only (`apps/web`, plus `docs`), the **front desk's visits** screen for a space's owner and its
reception staff: the list of people present now (re-read every 30 s while the page is visible), the live
status control with its manual override, checking a visitor in by name, checking a visitor out with the
server's price quote and a money block (amount received, change, the unpaid rest left to a customer by phone),
a price typed by hand with a required reason or an unpriced close, one idempotency key per user intent, a
bottom action bar on phones, and «تبديل الموظف» (switch staff: sign out, back to sign-in). The API it calls is
already built and merged; **this PR changes no API code.**

- **PR:** #116 · **head:** `30c48633c74163a4f3b69032853bd8ecbd459b30` · **base:** `origin/main` · 90 files, 4
  commits (the owner accepted 90 files in one PR).
- **The approved plan:** `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\2_PLAN.md` (long; read only the parts §3
  names). **The owner's approval note at its top binds and wins** where the plan below it differs.
- **The executor's prompt and report:** `3_EXEC_PROMPT_PR1A.md` and `4_REPORT_PR1A.md` (same folder).

## 1. Rules — read-only, always

- **Never** edit, create or delete a file in the repository; never `git checkout`, `git switch`, `git reset`,
  `git stash`, `git commit`, `git push`, `git rebase`; never install anything (`npm ci`/`npm install`); **never
  run `npm`, `node`, `npx`, tests, builds or servers**; never touch a database; never comment on GitHub.
- **Allowed commands only** (PowerShell, from `C:\dev\masaha\app-design`): `git fetch origin`, `git log`, `git
  show`, `git diff`, `git grep`, `git ls-tree`, `git merge-tree`, and read-only `gh pr view` / `gh pr checks`.
  Read files in the workspace folder named above with your file reader.
- **Read every repository file at the head's sha, never from the working tree** (the working tree is an older
  commit): `git show 30c48633:<path>`. If two reviewers fetch at once a `git` command may fail on a `.lock`
  file: wait 30 seconds and run it again once; never delete a `.lock` file.
- **Report concrete problems only**, each verified by reading the code: the file and line (at `30c48633`), the
  scenario (what a user does → what goes wrong), the severity, and the fix. If you are not sure, write
  **"plausible"** and why. Say clearly what you **saw in the code** and what you only **read in the executor's
  report**. No praise. No mention of any AI tool's name inside findings.
- **Severity:** **blocker** (wrong money recorded or shown, a double payment or a double visit, a page that
  breaks, a security or privacy hole, a test that cannot fail) · **should-fix** (a real defect a user can meet;
  a missing planned test; a document that says something false) · **nit** (style, wording, small cleanup).
- **Do not report** what lint, typecheck, Prettier or CI already enforce and passed (formatting, unused
  imports, type errors); CI is green on this head.

## 2. First steps (in this order)

```powershell
cd C:\dev\masaha\app-design
git fetch origin
gh pr checks 116
gh pr view 116 --json headRefOid,mergeStateStatus,files
git fetch origin pull/116/head
git log --format="%h %s%n%b" origin/main..30c48633
git diff --stat origin/main...30c48633
```
If a check is red or pending, or the head is not `30c48633…`, write that at the top of your report and stop.
Write in the report: the head, the checks, the commit subjects with their lengths (each must be ≤ 50
characters and have a body), and whether any commit message names an AI tool or has a `Co-Authored-By` line.

## 3. What to read (and only this)

1. `git show 30c48633:CLAUDE.md` — the project's rules (they bind the code you review).
2. In `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\2_PLAN.md`: the **approval note at its top**; §1; §2 *Scope*,
   *Acceptance criteria* and *Out of scope* for **PR 1**; §4; §5 (S1–S13); §8 *PR 1 — the desk's visits* (design
   issues DI-n); §10 *PR 1 · Commits 1–4*; §11 *PR 1* — **tests 1–30 and 40** (tests 31–39 and 41 belong to PR
   1b, not this PR); §13 *The real run* (PR 1a's writes only).
3. `4_REPORT_PR1A.md` — its *Departures* section and its run results.
4. The code: every file of the diff (`git diff origin/main...30c48633 -- <path>` per file or folder). Work
   through them in this order, one group at a time:
   - **A. The key:** `apps/web/src/shared/api/idempotency/*`, `apps/web/src/shared/api/client/request.ts` and
     its test, `apps/web/src/shared/api/index.ts`.
   - **B. The shell:** `apps/web/src/pages/dashboard/shell/{DashboardLayout,PageActionBar,PageActionSlot}*`,
     `apps/web/src/shared/routing/actionBar/actionBarShown.ts`, `apps/web/src/shared/routing/index.ts`,
     `apps/web/src/app/providers.tsx`.
   - **C. Occupancy:** everything under `apps/web/src/features/occupancy/`.
   - **D. The desk:** everything under `apps/web/src/features/desk/` (repository, services, hooks, components),
     and `apps/web/src/test/deskVisit.ts`.
   - **E. The page:** `apps/web/src/pages/dashboard/space/desk/*`, `apps/web/src/pages/dashboard/routes.tsx` and
     its test.
   - **F. Words:** `apps/web/src/shared/copy/{arabic,english}/{desk,occupancy,index}.ts`.
   - **G. Documents:** `docs/features/{desk,occupancy,visits}.md`, `docs/frontend/architecture.md`,
     `docs/project/overview.md`, `docs/README.md`, `docs/architecture/findings/README.md`,
     `docs/architecture/findings/161-no-route-reads-the-visits-of-a-day.md`.
   To check what the server really answers, read the shared types it uses:
   `git show 30c48633:packages/shared/src/<module>/<file>.ts` for `desk`, `visits`, `occupancy`, `payments`,
   `core` — and `docs/api/api-contract.md` (*Front desk (managed)*, *Occupancy (managed)*, §6 the error codes).

## 4. The checklist — answer every line in your report (✔ seen / ✘ finding / ? could not tell, and why)

**4.1 The idempotency key (money safety: a retry must never record twice)**
- One key per user intent: created when the dialog opens (or the intent starts), **the same key** on every
  retry and on a double press, a **new key** only after a success or when the user starts a new intent. Find
  where the key is renewed: is it renewed on an error? (it must not be, or a retry after a lost answer records
  twice).
- Is the key ever renewed while the form is edited in a way that changes the payment? The plan's S4 says what
  happens; check the code does exactly that.
- Every create the server marks with a key (`Idempotency-Key` in the contract: the visit's check-in, check-out,
  and a payment) sends it — read `deskRepository.ts` and its test. Requests the contract says take **no** key
  must not send one.
- The transport's automatic re-sends (the report says it re-sent twice when offline) reuse the same header.
- A lost answer (network error, timeout) shows a line saying a retry is safe; it does not silently re-send by
  itself beyond the transport's rule.

**4.2 Money (agorot are integers; the server is the only source of a charge)**
- No charge, due or price is **computed** in the browser as the truth: the due comes from the server's quote;
  check `moneyOf.ts`, `useMoneyBlock.ts`, `MoneyBlock.tsx`, `CheckOutDialog.tsx`.
- "Received now" defaults to the due; the amount **sent** is never above the due for a visit (change is shown,
  not recorded); a typed amount above the due shows change, and the request carries the due.
- The quote: re-read every minute while the dialog is open, and re-read before sending when older than 4
  minutes (`quoteAge.ts`: is the boundary exactly the plan's?); if the due changed, the send stops and says so.
- An unpaid remainder on a visit with no customer requires a name and a phone before sending.
- A visit with no rate: whoever may type a price types an amount **and a reason** (required); whoever may not
  closes it unpriced (phone required). Where does the web learn who may type? (It must be the server's
  `mayTypePrice` from the visit terms, never a guess from the role.)
- Every amount is displayed through the project's money formatter, with the right direction (left-to-right
  digits inside Arabic text).
- The toasts name the amount, method and remainder **from the server's answer**, not from the form.

**4.3 Authorization and roles (hiding a button is never authorization)**
- What the owner sees and reception does not (the override? a typed price?) — is every such case also refused
  by the server (read the contract)? A 403 from the server shows a line ("no longer open to you"), not a crash.
- Nothing in the page reads a route reception may not read (for example the space's settings, owner-only).

**4.4 The present list and the live status**
- Re-read every 30 s **only while the page is visible**, and on returning to it; **never while hidden** (look at
  the query's options: `refetchInterval`, `refetchIntervalInBackground`, `refetchOnWindowFocus`).
- A failed refresh keeps the rows already shown (not replaced by an error); a first failure shows its error with
  a retry.
- Durations ("since", "2 h 05 m") and the override's time left are computed from the server's times; Gaza time,
  not the browser's zone, where a day or a clock is shown (`currentShift.ts`, `stayDuration.ts`,
  `overrideLeft.ts`): check midnight and the zone.
- The live status control: disabled with its reason while the space is closed; `SPACE_NOT_OPEN` said; the
  override's choices (30 min, 1 h, 2 h, until closing) and «back to automatic».
- «27 / 40» capacity shown as settled, and no money total of uncollected visits (DI-3).

**4.5 The bottom action bar and the toasts (the owner's approved departure)**
- Below 768 px the page's main action sits in a bottom bar and the content gets room so nothing is hidden under
  it; from 768 px it is in the top bar. The toasts are raised above the bar through a small store in
  `shared/routing` read by `app/providers.tsx`: is that store reset when the page leaves (no stale offset on
  another page)? Does it respect the architecture's layers (a `shared/` module must not import a `features/` or
  `pages/` module)?

**4.6 Accessibility and right-to-left**
- One `h1` per page; each section named by its heading; dialogs titled; the focus goes into a dialog on open
  and back to the control that opened it on close; buttons have names (including icon-only «⋯» menus, named
  by the row); the money block is a named group.
- Touch targets at least 44 px on touch screens (the report says 44/44/48 px measured).
- Only **logical** direction classes (`ps-`, `pe-`, `ms-`, `me-`, `start-`, `end-`), never `pl-`/`pr-`/`left-`/
  `right-` (CI's `check:classes` passed — only report what it cannot catch, e.g. an icon that must mirror).
- Names in the other language carry `lang`/`dir`.

**4.7 Words (every user-facing string in both catalogues)**
- No hard-coded user-facing text in any component or hook (search the diff for quoted Arabic or English
  sentences outside `shared/copy`).
- Every new line exists in both `arabic/` and `english/`, with the same keys; counted lines use the plural
  helpers (Arabic six forms).
- The two lines the executor added (`«خروج»` and `«خروج {name}»`) are needed and not duplicates.
- Every error code the contract lists for these routes (§6 of the contract, for check-in, quote, check-out,
  payment, override) has a worded line — list any code with no line.

**4.8 Tests (each must be able to fail)**
- For each test 1–30 and 40 of the plan's §11 *PR 1*: does it exist (file and title), and does it check what
  the plan says? Write a table: test number → file → present / missing / weaker than planned.
- For the tests the plan marks as key, money, role, state, warn: would its break (the plan's last column) really
  make it fail? Look for tests that assert nothing meaningful, mock the very thing under test, or wait on fake
  timers in a way that passes either way.
- The report says breaks 7, 26, 29 were replaced (the planned break "couldn't change the outcome"): judge each.
- The report says two tests (App › "renders the main landmark", router › "shows the root's general error…")
  timed out at 3 s locally and passed alone and in CI: is that a test defect (a cold lazy import inside a 3 s
  wait) or a slowness of the app? Plausible is fine.

**4.9 Architecture and scope**
- The project's layers: `shared/` never imports `features/` or `pages/`; one feature does not import another
  feature's internals (only its `index.ts`); `features/desk` is dashboard-only and never reaches the public
  site's first download (CI's `check:build` passed — report only a path it cannot see).
- Nothing outside the plan's PR 1a scope: no PR 1b work (uncollected visits, write-off, unpriced pricing), no
  API or `packages/shared` change, no design-system file changed without its label.
- Only the design system's semantic tokens for colours and sizes (no raw colours, no arbitrary values).
- The plan's findings for PR 1 (§2 *Scope* names 160–164): only **161** was written. Are the others owed in this
  PR, or later? Say which and why from the plan.

**4.10 Documents (true to the code; one home per fact)**
- `desk.md`, `occupancy.md`, `visits.md`: their web parts describe what this PR built, no more (nothing of PR
  1b, nothing "planned" written as "built"); decision and history lines end with a date and `#116`.
- `architecture.md`: the new rules it states (the bottom bar, one key per intent, the desk's polling, S1's
  feature exception) match the code.
- `overview.md` *Built* lines and `docs/README.md`: true and not duplicated.
- No `#PRNUM` left (`git grep -n PRNUM 30c48633 -- docs apps`).

**4.11 The executor's departures** (from `4_REPORT_PR1A.md`) — judge each: accepted / not accepted, why.

## 5. The report's shape

```
# Review — DESK_SCREENS PR 1a (#116) — <Codex | OpenCode>
Head: <sha> · checks: <green/red> · head moved during the review: <yes/no>
Verdict: <mergeable | mergeable after small fixes | not mergeable>

## Findings (most severe first)
### F1 — <blocker|should-fix|nit> · <one-line title>
- Where: <file>:<line> at 30c48633
- Seen in the code: <what>      (or: Only in the report: <what>)
- Scenario: <user action → wrong result>
- Fix: <what to change>
...

## Checklist 4.1 – 4.11
<each line: ✔ / ✘ (→ F<n>) / ? (why)>

## Tests table (4.8)
| # | file | present / missing / weaker |

## Departures judged (4.11)

## Not checked, and why
```

At the very end run `gh pr view 116 --json headRefOid` again and fill "head moved". Then stop.
