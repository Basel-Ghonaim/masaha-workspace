# Review — DESK_SCREENS PR 2 (#119, `feat/desk-subscribers`): one independent reviewer, read-only

You are an **independent code reviewer** of one pull request in the Git repository at
`C:\dev\masaha\app-design`. This file is self-contained: every command, file and question is written here. You
did not write the code; another agent did. **Trust nothing you have not seen in the code.**

**Your report file** (write only this file, nothing else anywhere):
`C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\6_REVIEW_PR2_<TOOL>.md` — `<TOOL>` is `CODEX` or `OPENCODE`,
whichever you are. Write it **as you go** (a section after each part of §4), so nothing is lost if you stop
early.

## 0. What the PR is

Masaha is a bilingual (Arabic right-to-left / English) web platform for coworking spaces. PRs #116 and #117
(merged) built the front desk's visits, uncollected and unpriced cards. **This PR adds the desk's subscribers,
in the web app only (`apps/web`, plus `docs`):**
- **The one search (K1):** once typing pauses (400 ms), first the people **present** who match (by a part of
  the name, or a subscriber's phone's last two digits or more), then the **customers** the server's customers
  list finds (the present ones left out), each a card with phone, subscription status and end, and balance;
  then «تسجيل زيارة باسم «X»», the visit's check-in with the typed name.
- **A subscriber's check-in («حضور»)**: one tap with one idempotency key when the current subscription runs;
  with none, an expired or a not-started one, a choice first — a visit by their name (not added to their file,
  finding 160) or the check-in anyway. **Check-out («خروج»)**: one tap, **no key**; the toast says the stay and
  what the subscription still owes, with «استلام».
- **«استلام دفعة» — a payment on one item**: from the page (the customers who owe, those present first), a
  card's «استلام {amount}», or the check-out toast; one payment on one item (an unpaid visit or an owing
  subscription), one key per opening; the amount follows the chosen item until typed; a usage-based
  subscription may take more, as credit.
- **Carried from #117:** the uncollected card keeps its page in range (`usePageInRange`).

The API is built and merged; **this PR changes no API code and no `packages/shared` code.** #118 (merged during
the work) added reception's idle sign-out (`SESSION_IDLE`) and subscribing from a published price; PR 2 reads
neither.

- **PR:** #119 · **head:** `8d087c5ede6dd5406148258477beb8b4e4106fd9` · **base:** `origin/main` · 65 files, 5
  commits.
- **The approved plan:** `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\2_PLAN.md` (long; read only the parts §3
  names). **The owner's approval note at its top binds and wins** where the plan below it differs.
- **The executor's prompt and report:** `3_EXEC_PROMPT_PR2.md` and `4_REPORT_PR2.md` (same folder). The executor
  worked part of the time under the owner's autonomy rule (`C:\dev\masaha\workspace\_SHARED\
  AUTONOMY_2026-10-25.md`): it took some decisions alone; they are in the report's last sections — judge them.

## 1. Rules — read-only, always

- **Never** edit, create or delete a file in the repository; never `git checkout`, `git switch`, `git reset`,
  `git stash`, `git commit`, `git push`, `git rebase`; never install anything; **never run `npm`, `node`, `npx`,
  tests, builds or servers**; never touch a database; never comment on GitHub.
- **Allowed commands only** (PowerShell, from `C:\dev\masaha\app-design`): `git fetch origin`, `git log`, `git
  show`, `git diff`, `git grep`, `git ls-tree`, and read-only `gh pr view` / `gh pr checks`. Read the workspace
  files named here with your file reader.
- **Read every repository file at the head's sha, never from the working tree** (it is an older commit): `git
  show 8d087c5e:<path>`. If a `git` command fails on a `.lock` file, wait 30 seconds and run it again once;
  never delete a `.lock` file.
- **A finding is a defect you verified, nothing else.** Each one needs: the file and line (at `8d087c5e`), the
  scenario (what a user does → what goes wrong), the severity, and the fix. **Do not list as a finding** a point
  whose own conclusion is "no change needed", a departure you accept, or the plan's own wording: those go in
  the checklist or the departures section. If you are not sure, write **"plausible"** and why. Say clearly what
  you **saw in the code** and what you only **read in the executor's report**. No praise.
- **Before calling something a bug, check the library's defaults** (for example TanStack Query v5:
  `refetchIntervalInBackground` is `false` by default; `placeholderData: keepPreviousData` keeps the last data
  while the next loads; a query with `enabled: false` sends nothing). A finding built on a wrong assumption
  about a library is worse than no finding.
- **Severity:** **blocker** (wrong money recorded or shown, a double payment or a double check-in, a page that
  breaks, a security or privacy hole, a test that cannot fail) · **should-fix** (a real defect a user can meet; a
  missing planned test; a document that says something false) · **nit** (style, wording, small cleanup).
- **Do not report** what lint, typecheck, Prettier or CI already enforce and passed; CI is green on this head.

## 2. First steps (in this order)

```powershell
cd C:\dev\masaha\app-design
git fetch origin
gh pr checks 119
gh pr view 119 --json headRefOid,mergeStateStatus,files
git fetch origin pull/119/head
git log --format="%h %s%n%b" origin/main..8d087c5e
git diff --stat origin/main...8d087c5e
```
If a check is red or pending, or the head is not `8d087c5e…`, write that at the top of your report and stop.
Write in the report: the head, the checks, the five commit subjects with their lengths (each ≤ 50 characters,
each with a body), and whether a commit message names an AI tool or has a `Co-Authored-By` line.

## 3. What to read (and only this)

1. `git show 8d087c5e:CLAUDE.md` — the project's rules (they bind the code you review).
2. In `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\2_PLAN.md`: the **approval note at its top**; §2 *Scope*,
   *Acceptance criteria* and *Out of scope* for **PR 2**; §5's S2, S3, S4, S6, S10 (search them); §8 *PR 2* (the
   design issues DI-14, DI-20, DI-21, DI-22, DI-31, DI-35, DI-36, DI-38, DI-40); §10 *PR 2 · Commit 1* to
   *Commit 4*; §11 *PR 2* — **tests 42–53**.
3. `4_REPORT_PR2.md` — every *Departures in commit n* list, *A fix after the head's lanes*, *The real run*, and
   *Decisions taken without the owner*.
4. The contract: `git show 8d087c5e:docs/api/api-contract.md` — the sections for `GET …/customers` (its `q`),
   `GET …/customers/:customerId` (the file), `POST …/check-ins` (the subscriber's check-in, its key and
   warnings), `POST …/check-ins/:checkInId/check-out`, `GET …/check-ins?open=true`, `POST …/payments`, and §6's
   codes (`MEMBER_ALREADY_CHECKED_IN`, `CUSTOMER_ARCHIVED`, `PAYMENT_EXCEEDS_DUE`); the shared types under
   `packages/shared/src/{customers,subscriptions,payments,desk}/` that the web imports.
5. The code: every file of the diff, one group at a time (`git diff origin/main...8d087c5e -- <path>`):
   - **A. Data:** `apps/web/src/features/desk/repository/deskRepository.ts` and its test,
     `apps/web/src/features/desk/hooks/queryKeys.ts`, the open check-ins query.
   - **B. The search:** `apps/web/src/features/occupancy/` (`matchesPerson`, `usePresentMatches`,
     `PresentMatches`), `features/desk/hooks/search/*`, `components/search/*`, the customer card,
     `services/{balanceView,statusView,dayText}.ts`.
   - **C. Subscriber in and out:** `hooks/subscriber/*`, its dialog and toasts, `services/progressLines.ts`.
   - **D. The payment:** `services/openItems.ts`, `hooks/pay/*` (or the plan's `usePayDialog`), `PayDialog`.
   - **E. Carried:** the uncollected card's `usePageInRange` change and its test.
   - **F. The page and words:** `apps/web/src/pages/dashboard/space/desk/DeskPage.tsx`,
     `apps/web/src/features/desk/index.ts`, `apps/web/src/shared/copy/{arabic,english}/{desk,occupancy}.ts`,
     the routes test's fake server change (`git grep -n "check-ins" 8d087c5e -- apps/web/src/**/routes*`).
   - **G. Documents:** `docs/features/{desk,customers,payments,subscriptions}.md`,
     `docs/architecture/findings/README.md` and finding 160.

## 4. The checklist — answer every line (✔ seen / ✘ finding / ? could not tell, and why)

**4.1 Keys and repeats — no double check-in, no double payment**
- A subscriber's check-in: one key per tap, kept across a retry and a double press, **never renewed on an
  error**, sent as `Idempotency-Key`; the button cannot send twice while busy.
- The check-out sends **no** key and is **never retried automatically** (the transport retries only keyed
  writes): a lost answer says so and lets the user decide.
- «استلام دفعة»: one key per opening of the dialog; one payment per submit; changing the item after an error —
  does the same key go out for a **different** body (a server conflict), and is that handled or impossible?
- «تسجيل كزيارة» from the pre-check-in choice uses the visit check-in's own key, not the subscriber's.

**4.2 The search**
- One request once typing pauses (not per key); `q` only once it is 1–60 characters; an empty term asks
  nothing and shows no group; a stale answer for an older term can never replace a newer one's (query keys by
  term, or as built).
- The present group: a name's part (Arabic folding as built — a departure says plain `includes`: does it miss a
  common case such as «أ»/«ا»?), phone digits only for a check-in, never a visit; the customers present are left
  out of the second group, so no person appears twice.
- The visit button is primary only when nothing matched (DI-20); the no-match line promises no customer file
  (DI-36).
- **The departure:** a present customer appears only in the first group, so a card never shows «خروج» or a
  presence badge. Can the staff still check that customer out from the search? Say what a user sees.

**4.3 The subscriber's check-in and check-out**
- `ACTIVE` and `ENDING_SOON` check in at once; none, expired and not-started open the choice; "anyway" is not
  offered with none. The not-started date is read from the customer's file (a departure, the owner's answer):
  is the file read only when needed, and what does the dialog say while it loads or if it fails?
- `MEMBER_ALREADY_CHECKED_IN` and `CUSTOMER_ARCHIVED` worded; the server's warnings said after, in the toast
  (S6); the search cleared and focused after (S10).
- The check-out toast: the stay from the answer's `checkedInAt`/`checkedOutAt`; «يبقى {amount}» only when the
  subscription's balance is above zero; «استلام» opens the payment on **that** subscription; the focus goes to
  the next row's «خروج» (DI-31), never to `body`.
- The present list's usage line is the subscription's first progress line (`progressLines`), refetched when the
  present check-ins change (S2).

**4.4 The payment («استلام دفعة») — money**
- `openItems`: unpaid visits oldest first, an unpriced visit left out, then subscriptions that owe; a
  usage-based subscription with no balance offered only when chosen from its card.
- The amount follows the chosen item only while untouched (DI-35); it is never sent above what a **fixed** item
  owes (`PAYMENT_EXCEEDS_DUE` worded if it is); a usage-based item may take more, said as credit.
- The page's list: the customers who owe, present first (DI-21). The executor did **not** show this live (no
  demo data, decision 1); judge whether test 53 really proves the order.
- After a payment, which query keys are invalidated: the search's cards, the file, the uncollected card, the
  present list's line? A stale balance left on screen is a should-fix.

**4.5 Dates, words, accessibility, RTL**
- `dayText` formats a `YYYY-MM-DD` date at its UTC midnight in `timeZone: 'UTC'` (the plan said `Asia/Gaza`, a
  departure): is the day shown always the date's own day, in any browser zone?
- Every user-facing string in both catalogues with the same keys; counted lines through the plural helpers
  (`search.found`); no hard-coded text in components or hooks; the phone `dir="ltr"`; names in the other
  language carry `lang`/`dir` (the report's late fix of the Arabic name on the English card: check it).
- The search `role="searchbox"`, named, `aria-controls` the results; groups `h2`, cards `h3` (DI-38); the count
  `aria-live="polite"`; focus on arrival from 768 px only; dialogs titled, focus in and back.

**4.6 Tests (each must be able to fail)**
- For each test 42–53 of the plan's §11 *PR 2*: present / missing / weaker than planned, with its file.
- Tests 42, 43, 44 and 51 count their red step as their break: would a regression after the code exists still
  turn them red?
- The routes test's fake server now answers `GET …/check-ins?open=true`: does it hide anything a real test
  should see?

**4.7 Architecture, scope, documents**
- `shared/` never imports `features/` or `pages/`; `features/desk` imports other features only through their
  `index.ts` (`occupancy`'s `PresentMatches`); no API or `packages/shared` change; semantic tokens only.
- `desk.md`, `customers.md`, `payments.md`, `subscriptions.md`: their web parts describe what this PR built and
  no more; decision and history lines end with a date and `#119`; no `#PRNUM` left (`git grep -n PRNUM
  8d087c5e -- docs apps`).
- Finding 160: what it says is true to the code; its index line present.

**4.8 The executor's departures and its decisions taken without the owner** (from `4_REPORT_PR2.md`) — judge
each: accepted / not accepted, why.

## 5. The report's shape

```
# Review — DESK_SCREENS PR 2 (#119) — <TOOL>
Head: <sha> · checks: <green/red> · head moved during the review: <yes/no>
Verdict: <mergeable | mergeable after small fixes | not mergeable>

## Findings (verified defects only, most severe first)
### F1 — <blocker|should-fix|nit> · <one-line title>
- Where: <file>:<line> at 8d087c5e
- Seen in the code: <what>      (or: Only in the report: <what>)
- Scenario: <user action → wrong result>
- Fix: <what to change>
...
(If there is none, write "None.")

## Checklist 4.1 – 4.8
<each line: ✔ / ✘ (→ F<n>) / ? (why)>

## Tests table (4.6)
| # | file | present / missing / weaker |

## Departures and decisions judged (4.8)

## Not checked, and why
```

At the very end run `gh pr view 119 --json headRefOid` again and fill "head moved". Then stop.
