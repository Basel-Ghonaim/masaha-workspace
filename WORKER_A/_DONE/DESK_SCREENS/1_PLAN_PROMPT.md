# DESK_SCREENS — the front desk and the subscribers on the web: Front desk, Customers, Customer details, New / renew subscription (build map steps 7 and 8's screens, screens 13–16) — PLAN ONLY

**No branch, no checkout, no file edit in the repository, no commit, no install, no test run, no
server, no database command.** You write one file — the plan — then stop.
**No trial build anywhere either:** no temporary copy of the repository, no `git worktree add`, no
`git stash`, no scratch or temp folder holding code, no `node` / `tsx` / `tsc` / `vitest` / `psql` /
`npm` run — not in the repository, not in a scratchpad, not in a temp directory. The only commands are
`git fetch`, `git show`, `git log`, `git ls-tree`, `git grep`, `git diff` between commits, read-only `gh`,
and reading files. Where you are unsure that something works, write it in the plan as **a check the
executor makes first, with what to do if it fails** — never try it yourself. Read only the files the plan
needs, each once. **This is a plan, not a Work Item's execution:** do not run the `start-work-item` skill (the
owner's instruction); if you are Claude Code, use `write-plan` only for its discipline (save the file; no
plan-mode step is needed).

**The task's folder:** `C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\`. This prompt is `1_PLAN_PROMPT.md`;
**save the plan as `2_PLAN.md` here**; reports will be `4_REPORT_PR<n>.md`.

**Where you read.** `C:\dev\masaha\app-design` — commit objects only: `git fetch origin`, then `git show
origin/main:<path>`, `git ls-tree`, `git grep origin/main`. Never check anything out, switch or reset it: a
small task (`chore/conflict-guard`) may hold a branch there, and reviewers read there too. If a `git` command
fails on a `.lock` file, wait 30 s and retry once. Worker A's `C:\dev\masaha\app` and worker B's
`C:\dev\masaha\app-b` — never work there.

## 0. The base and what runs beside it

Plan from today's `origin/main` (write its sha in the plan's header). **Beside it:**
- **Worker B** — ANNOUNCEMENTS PR 1 (#112, open: announcements, `CLOSURE_IN_FORCE` at both check-ins, the
  public page's announcements; `gh pr view 112`), then **step 9's API** (payments voided, balances, credit,
  each staff member's collections today — not planned yet), then ANNOUNCEMENTS PRs 2–4. Read #112's diff
  (`git fetch origin pull/112/head`) for what the desk will show of a closure; state in the plan what is built
  only once #112 has merged (an executor check).
- **Worker A** — the public site's fix PR after the owner's in-person review (`WORKER_A\PUBLIC\
  0_CARRIED_FROM_111.md` plus the owner's list; `apps/web/src/pages/site`, `features/directory`). **This plan's
  executor starts after that PR has merged**; its first step is `git diff --name-status <the plan's base>
  origin/main` — a code file the plan names changed in a way the plan does not cover → stop and ask.
- **`TASKS\CONFLICT_GUARD_BASEL`** (CI and documents) and later **`TASKS\DEMO_DAILY_BASEL`** (the demo seed
  renews a FULL space and a closed-today space on every run). The desk's real run needs a space FULL and one
  closed today: say which case needs which, and make "DEMO_DAILY merged, or the data holds the case today" an
  executor check.
- **Finding numbers:** this item's start at **160** — write `160`, `161`, … in the plan.

## 1. The plan must stand alone

Fresh conversations execute each PR (Claude Code or another capable coding agent — no step may depend on a
Claude skill; an appendix maps steps to skills, "only a map"), and another conversation reviews each (one
reviewer, no subagents). Every decision with its one-line reason; the files; each component, hook, query,
mutation and type with its interface; the words in both catalogues (Arabic plurals through the catalogue's
plural forms; every line in both languages; the Arabic for the owner's approval); each test with its lane,
title and the break that must make it fail (`docs/development/testing.md` §3 — **every break run and its red
output recorded**); **each permission shown or hidden by role, each money figure, each idempotency key and
retry, each warning, each state (loading, empty, failure, offline, a conflict answered 409), each width and
each accessibility rule gets a deliberate break**; the commits, subjects counted (≤ 50); fixes before the push
folded (`--fixup` + autosquash, `GIT_SEQUENCE_EDITOR=:`); every new decision and history line ends with its date
and `#PRNUM`; the procedure with its commands — as `C:\dev\masaha\workspace\WORKER_A\PUBLIC\2_PLAN.md` §13 has
them (branches from the latest `origin/main` in `C:\dev\masaha\app`, `--no-track`; `docker start
masaha-postgres-1`, never `db:up`, never `npm ci`; the API on 3320 and the web on 5320 with worker A's
`masaha_dev`; **memory: one full test run at a time on this machine, none while a `vitest` of
`C:\dev\masaha\app-b\` runs, the free memory recorded before each full lane; the known exceptions — finding
87's routes test and a lane killed for memory, re-run once, then CI judges**; per commit `lint` + `typecheck`;
on the head once `test:unit`, the scoped `test:component`, the production build (`$env:NODE_ENV='production'`),
`check:build` (the desk's code stays out of the site's first download), `check:classes`, `format:check`,
`check:links`; a real run with **real screenshots** (local headless Chrome over CDP, as
`WORKER_A\PUBLIC\scripts\run2b.mjs` — Enter sent with `text: '\r'`), as the owner and as reception, Arabic
light and English dark at 390, 768 and 1440 for the layouts that change with width, screenshots to this
folder's `shots\pr<n>\`; `#PRNUM` replaced per commit tree by a self-checking script
(`WORKER_A\PUBLIC\scripts\prnum3b.sh` the model); push; `gh pr create --assignee @me --label feat --label
area:web --label area:docs`; `gh pr checks` and `CLEAN`; the conflict check); a **"Stop and ask"** list; the
executor's stop rule (**a test it cannot run stops the work** — the wording of `WORKER_A\PUBLIC\
3_EXEC_PROMPT_PR4.md` §2, its break clause and its exceptions included); **a demo account or demo data that does
not hold what a real-run case needs → stop and report, never change data through the app to get past it** —
the desk's real run itself writes check-ins, visits and payments: name each write and its demo account; the
executor's scripts in this folder's `scripts\`, never committed; **carried items:** a
`0_CARRIED_FROM_<n>.md` from the previous PR's review, if any, is that PR's first commit. Never merge; no tool
attribution; stage by path.

## 2. The owner's decisions (2026-10-24)

**The goal (screens 13–16, `docs/design/SCREENS.md` *Owner and reception dashboard*):** the owner and reception
run the day at the desk — check visitors and subscribers in and out, see who is present and the live status
with its override, quote and take a visit's payment, deal with unpriced and uncollected visits; keep customers
on file, read a customer's file (subscriptions, statement, payments, debts), and make or renew a subscription.
**The API is built** (steps 7 and 8: #94, #95, #97, #100, #102, #106, #109, #110); the dashboard shows a
placeholder for each of these pages today.

1. **Worker A builds it** — the item is the web's.
2. **One plan for the four screens** (they share the desk's state, the customer and the subscription; one plan
   holds them together), **cut into PRs in sequence**, each cut from `main` once the one before it has merged.
   The supervisor's suggested cut, for you to confirm or better: **PR 1** the desk's visits (check-in by name,
   present list, live status and override, check-out with the quote and the first payment, unpriced and
   uncollected visits, a visit's later payment); **PR 2** the desk's subscribers (find a customer, check in with
   the warnings, check out, the open check-ins); **PR 3** Customers and Customer details (the list, the file,
   archive and restore, the statement, the debts, a payment); **PR 4** New / renew subscription (the sheet).
   Each PR ≈ 60 files at most; a better cut goes to *Proposed alternatives*, with why.
3. **Allocation preview (finding 125):** the subscription's sheet wants to show how a payment will be spread over
   the customer's older debts before it is saved, and the API does not expose the allocation's order. **Compare**
   (a) the answer carrying each item's `createdAt` so the web computes the order, (b) a quote route answering
   the allocation as the server will do it, and (c) no preview (the result shown after saving); recommend one.
   **Any API change is not this item's:** write it as a short, self-contained API spec for worker B (route or
   field, the rule, the tests, the documents), to merge **before** the PR that uses it.
4. **The statement's snapshot (finding 124):** the file's sums and its listed payments read in one `REPEATABLE
   READ` transaction — an API fix for worker B, specified in the plan like point 3, merged before the
   Customer details PR.
5. **The shared desk device (`_SHARED\OPEN_DECISIONS.md` point 4) — revised by the owner, 2026-10-24:** the
   2026-10-20 line said "a web behaviour"; the owner now holds that a sign-out only in the browser protects
   nothing (the session stays valid on the server; authorization lives on the server). So: **reception's
   session ends after 15 minutes idle on the server** (an API change for worker B, specified like point 3:
   where the idle time is kept, what renews it, the answer the web gets, its tests) **and** the web shows
   «تبديل الموظف» in the desk's top bar (sign out and return to sign-in) and handles the idle sign-out's answer.
   Propose the line that revises `OPEN_DECISIONS.md` point 4 — the supervisor edits it.
6. **The design's basis:** design review round 2 is not finished for the desk (its data-and-flow review, DK-DF,
   is not done; its summary and `DECISIONS_ROUND2.md` are not written). **Build from the settled decisions**
   (`C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_DESK.md`, `DECISIONS_SHARED.md`, and
   `DECISIONS_OWNER.md` where it names customers or subscriptions) **and read the six accepted round-2 desk
   reviews** — `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-DK-AX_REPORT.md`, `R2-DK-CP_REPORT.md`,
   `R2-DK-EX_REPORT.md`, `R2-DK-TR_REPORT.md`, `R2-DK-UX_REPORT.md`, `R2-DK-VD_REPORT.md`. **Do not copy a defect
   they prove** into the web; list each such point as a numbered **design issue** with the report and issue it
   comes from and its fix, **built only once the owner approves it** (as `WORKER_A\PUBLIC\2_PLAN.md` §8 does).
   Anything that would change a settled decision → a *Proposed alternative*, never applied.
7. **Step 9 comes next on the API** (worker B, after #112): payments voided, balances, credit and «دفعاتي اليوم»
   are **not built**. Name each part of screens 13–16 that needs step 9 (for example the desk's collections
   today, a payment's void) and leave it out of this item, without a dead control — or, if a part cannot be
   left out without harm, say so as a decision for the owner.
8. **The decisions above are proposals you may challenge** (the owner's rule): where you see a better way,
   argue it with evidence from the code or the documents in *Proposed alternatives*, with its cost — never
   apply it.

## 3. Read first

`CLAUDE.md`; `docs/development/workflow.md`; `testing.md`; `docs/frontend/architecture.md` (§1 zones, §2
routing and the dashboard's shell, §3 features, §5 errors, §7 the cache); `design-system/foundation.md` (§9
widths, §10 actions and accessibility, §12 components, §13 the dashboard's screens, §15 touch);
`localisation.md`; `documentation.md` §5; `docs/features/desk.md`, `visits.md`, `occupancy.md`,
`customers.md`, `subscriptions.md`, `payments.md`, `packages.md`, `space-settings.md`, `auth.md` (the session,
for point 5); `docs/api/api-contract.md` (§1–6, *Occupancy (managed)*, *Front desk (managed)*, *Customers
(managed)*, the subscriptions' routes, the payments' routes, the error codes and warnings); ADR 0008, 0009,
0010, 0015; `docs/backend/conventions.md` §13 (idempotency); `docs/plans/v1-mvp.md` steps 7–9;
`docs/design/SCREENS.md` (screens 13–16); the prototype: `docs/design/prototype/Desk.html`, `Customers.html`,
`Customer file.html`, `masaha/desk-core.jsx`, `masaha/desk-sheet.jsx`, `masaha/desk-data.js` and the shared
modules they use; the decisions files and the six reports of §2.6; `C:\dev\masaha\workspace\_SHARED\
OPEN_DECISIONS.md`; the findings index and findings 87, 124, 125; the code of `apps/web/src/pages/dashboard`
(the shell, the routes, the placeholders, the navigation per role), the dashboard features already built
(`features/staff`, `features/packages`, `features/space-settings`, `features/spaces` — the patterns to follow),
`shared/routing`, `shared/session`, `shared/forms`, `shared/lists`, `shared/copy`, `shared/api` (the
idempotency key's header), `packages/shared`'s `desk`, `visits`, `occupancy`, `customers`, `subscriptions`,
`payments` exports; `apps/web/scripts/` (`check:build`'s rules); `WORKER_A\PUBLIC\2_PLAN.md` as the model of a
web plan.

## 4. Decisions the plan must state (with a recommendation each)

- The features: which web features own what (`desk`, `customers`, `subscriptions`, `payments` — or fewer), what
  stays in `pages/dashboard`, and the dependency rule between them.
- The desk's state: what refreshes when (present list, live status, quotes) — polling or on return, by the
  model of decision 3 of `WORKER_A\PUBLIC\1_PLAN_PROMPT.md` — and the cache's keys and invalidations after each
  write.
- **Idempotency in the web:** one key per user intent, kept across a retry and a double press, a new key for a
  new intent; what the web shows on a retry's answer and on each 409.
- Money in the web: agorot end to end, the display, a typed price and its required reason (who may type one:
  `receptionMayTypePrices`), never a client-computed charge the server does not confirm.
- Roles: what the owner and reception each see and may press, **always backed by the server's answer** (hiding
  is never authorization); a 403 handled.
- Each width's layout against foundation §9, each state, and accessibility (names, landmarks, focus after each
  dialog and sheet, keyboard use of the desk at speed).
- Any document this decision set proves wrong — as a proposal, never applied silently.

## 5. The plan's shape

As `C:\dev\masaha\workspace\WORKER_A\PUBLIC\2_PLAN.md`: a header (base sha, worker, folder, the PRs with their
branch, size and title); summary; the contract per PR (scope, acceptance criteria, out of scope); the reading
done and what it changed; the decisions as built; stronger decisions (S…) and **Proposed alternatives**; the
API specs for worker B (points 3–5), each self-contained; related findings (folded or not, why); design issues
found in the reading (each with its fix, built only once the owner approves); the files; the interfaces and
the words; the tests with their breaks; the commits; the procedure and the stop rules; the decisions needed
from the owner (each with options and a recommendation). Stop after saving it, and reply only `PLAN READY:
C:\dev\masaha\workspace\WORKER_A\DESK_SCREENS\2_PLAN.md` with the PR count and the number of decisions for the
owner.
