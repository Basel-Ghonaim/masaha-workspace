# PAYMENTS_STEP10 — payments, announcements, data reports and favourites on the web (build map steps 9 and 10's screens: 17, 18, 23, 28, 10, 11 and the space page's parts) — PLAN ONLY

**No branch, no checkout, no file edit in the repository, no commit, no install, no test run, no server, no
database command.** You write one file — the plan — then stop.
**No trial build anywhere either:** no temporary copy of the repository, no `git worktree add`, no `git stash`, no
scratch or temp folder holding code, no `node` / `tsx` / `tsc` / `vitest` / `psql` / `npm` run — not in the
repository, not in a scratchpad, not in a temp directory. The only commands are `git fetch`, `git show`, `git log`,
`git ls-tree`, `git grep`, `git diff` between commits, read-only `gh`, and reading files. Where you are unsure that
something works, write it in the plan as **a check the executor makes first, with what to do if it fails** — never
try it yourself. Read only the files the plan needs, each once. **This is a plan, not a Work Item's execution:** do
not run the `start-work-item` skill (the owner's instruction); if you are Claude Code, use `write-plan` only for its
discipline (save the file; no plan-mode step is needed).

**The task's folder:** `C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\`. This prompt is `1_PLAN_PROMPT.md`;
**save the plan as `2_PLAN.md` here**; reports will be `4_REPORT_PR<n>.md`.

**Where you read.** `C:\dev\masaha\app-design` — commit objects only: `git fetch origin`, then `git show
origin/main:<path>`, `git ls-tree`, `git grep origin/main`. Never check anything out, switch or reset it (its working
tree is old; another planner and reviewers read there too). If a `git` command fails on a `.lock` file, wait 30 s and
retry once. Worker A's `C:\dev\masaha\app` and worker B's `C:\dev\masaha\app-b` — never work there.

## 0. The base and what runs beside it

Plan from today's `origin/main` (write its sha in the plan's header). **Not on `main` yet, read as merged** (each an
executor check at the start of PR 1):
- **#123** (worker B, the closure extension's API: `GET`/`POST …/announcements/:id/extend-subscriptions`,
  `CLOSURE_EXTENDED`, `CLOSURE_ALREADY_EXTENDED`) — if not on `origin/main`, read `origin/feat/closure-extension`
  (`ff8743c8`).
- **#124** (worker A, DESK_SCREENS PR 4, the subscription sheet — in its fix round) — read
  `origin/feat/subscription-sheet` for what the desk's pages and `features/desk` look like when this item starts.
  **This item's PR 1 starts after #124 has merged.**
**Beside it:**
- **Worker B** plans and builds **FINANCE_AUDIT** (step 11's API: the audit reader, platform settings, finance —
  `apps/api`, `packages/shared`, the web's two `errors.ts`, documents). Name every file both touch as a likely text
  conflict.
- **The public site's fix PR** (`WORKER_A\PUBLIC\0_CARRIED_FROM_111.md` plus the owner's list from his in-person
  review, still open): it touches `apps/web/src/pages/site` and `features/directory` — the same files as this item's
  PR 4. See §2's decision 3.
- **Finding numbers:** worker A's next free is **165** (check the findings index on `main`: 160–164 and 170–171 are
  taken) — write `165`, `166`, … in the plan.

## 1. The plan must stand alone

Fresh Claude Code conversations execute each PR, and another conversation reviews each (one reviewer, no
subagents). Every decision with its one-line reason; the files; each component, hook, query, mutation and type with
its interface; the words in both catalogues (Arabic plurals through the catalogue's plural forms; every line in both
languages; the Arabic for the owner's approval); each test with its lane, title and the break that must make it fail
(`docs/development/testing.md` §3 — **every break run and its red output recorded**); **each permission shown or
hidden by role, each money figure, each idempotency key and retry, each state (loading, empty, failure, offline, a
409), each width and each accessibility rule gets a deliberate break**; the commits, subjects counted (≤ 50); fixes
before the push folded (`--fixup` + autosquash, `GIT_SEQUENCE_EDITOR=:`); every new decision and history line ends
with its date and `#PRNUM`; the procedure with its commands — as `WORKER_A\DESK_SCREENS\2_PLAN.md` §13 has them
(branches from the latest `origin/main` in `C:\dev\masaha\app`, `--no-track`; `docker start masaha-postgres-1`, never
`db:up`, never `npm ci`; the API on 3320 and the web on 5320 with worker A's `masaha_dev`; **memory: one full test run
at a time, none while a `vitest` of `C:\dev\masaha\app-b\` runs, the free memory recorded before each full lane;
finding 87's family and a lane killed for memory — re-run once, then CI judges**; per commit `lint` + `typecheck` and
the touched test files; on the head once `test:unit`, the scoped `test:component`, the production build
(`$env:NODE_ENV='production'`), `check:build`, `check:classes`, `format:check`, `check:links`, `check:conflicts`;
**fix rounds run only the touched test files, never a full lane — CI judges** (the owner's rule, 2026-10-26); a real
run with **real screenshots** (local headless Chrome over CDP, as `WORKER_A\DESK_SCREENS\scripts\run3.mjs` on
`cdp3.mjs` — Enter with `text: '\r'`; **the script never keeps an `/auth/` request's body**), each role the PR
serves, Arabic light and English dark at 390, 768 and 1440 for the layouts that change with width, screenshots to
this folder's `shots\pr<n>\`, the run's writes named with their demo accounts; `#PRNUM` replaced per commit tree by a
self-checking script (`WORKER_A\DESK_SCREENS\scripts\prnum4.sh` the model) **and checked against the number `gh pr
create` answers** (worker B may open a PR meanwhile); push; `gh pr create --assignee @me --label feat --label
area:web --label area:docs` (`area:design-system` when it changes); `gh pr checks` and `CLEAN`; the conflict check);
the executor's scripts in this folder's `scripts\`, never committed; **carried items:** a `0_CARRIED_FROM_<n>.md` from
the previous PR's review, if any, is that PR's first commits. Never merge; no tool attribution; stage by path.

**How each PR is executed (the owner's decision 6 below):** under the owner's autonomy rule
(`C:\dev\masaha\workspace\_SHARED\AUTONOMY_2026-10-25.md`) — **no stop until ready for review**: a choice the plan
leaves open, a plan false against the code, a break that stays green, a real-run case the data cannot hold → decide,
record under *Decisions taken without the owner*, continue; a test or lane it cannot run → its exact error recorded,
the rest continues, CI judges; **no stop for the file count** (reported). The rule's hard limits hold (never merge,
never change data through the app to pass a case, never skip or weaken a test). Write the plan's procedure and its
"decide and record" list in that spirit — what the executor decides alone, and the few limits it never crosses.

## 2. The owner's decisions (2026-10-26) — binding

**The goal:** the screens of build map steps 9 and 10, on an API that is built — **step 9:** screen 17 *Payments*
(the owner's list with its filters and the void; reception's «دفعاتي اليوم», `Payments.html`, `My payments.html`;
API #114); **step 10:** screen 18 *Announcements* with the closure extension (`Announcements.html`; API #112, #123),
screen 23 the owner's *Data reports* and screen 28 the admin's (`Data reports.html`, `Admin reports.html`; API #120),
screens 10 *Favourites* and 11 *My reports* (`Favorites.html`, `Reports.html`; API #121, #120), and on the public site
the space page's announcements, its report button and dialog, and the favourite action on the cards and the page
(API #112, #120, #121). **The design is settled** in `C:\dev\masaha\workspace\DESIGN\DECISIONS\` — among them the void
the owner's alone with a reason, destructive (P9); «دفعاتي اليوم» striking a voided payment; O9–O12 (announcements,
end now / delete / start now / no end, the extension its own action once the closure started, the reporter anonymous
to the owner); A7 and AD-* for the admin's reports; C7–C8 and the account lines (favourites whole, «إزالة» with undo,
«الأقرب إليّ»); U8 and U10 on the space page (the sections' order; who reads a report). Build from them.

1. **One item, four PRs** — steps 9 and 10 together (step 9 is small; one plan saves a planning round).
2. **The cut and the order:** **PR 1** payments (the owner's page with its filters and the void; «دفعاتي اليوم» for
   reception); **PR 2** announcements with the closure extension (the owner's and reception's dashboard); **PR 3**
   data reports (the owner's page and the admin's); **PR 4** the user's side (Favourites, My reports, the report
   dialog, the space page's announcements, the favourite action on the cards and the page). Each cut from `main` once
   the one before merged. A better cut → *Proposed alternatives*, with why.
3. **PR 4 and the public site's fix PR:** PR 4 comes last. If the owner has finished his in-person review by then,
   the fix PR runs first and PR 4 builds on it; if not, PR 4 is built and the fix PR follows it. Plan PR 4 so either
   order works: name the files both touch.
4. **Finding 8** (the removable filter tag, which step 10 closes "at the start"): a design-system component, built as
   the first commit of the first PR that uses it (likely PR 3, the admin's reports filtered by space and field) —
   confirm from the code and the designs, or name the PR that does.
5. **Reviews:** a Claude review for PR 1 (money) and PR 2 (the extension moves subscriptions' ends); a free model's
   review for PRs 3 and 4. Write the review focus per PR so either reviewer can follow it.
6. **Execution under the autonomy rule, no stop until ready for review** (§1's paragraph).

**For you to decide, with a recommendation each (the owner approves):**
7. **The features:** which web features own what (`payments`, `announcements`, `data-reports`, `favorites` — or
   fewer; what `desk` already holds of payments), what stays in `pages/dashboard` and `pages/site`, and the dependency
   rule between them (`docs/frontend/architecture.md` §3).
8. **The cache and refreshes:** each list's keys and invalidations after each write (a void, a decision, an
   extension, a favourite saved from a card), and what refreshes when (the desk's model, `features/desk`'s keys).
9. **Idempotency in the web:** which writes carry a key (the void? an announcement's post — its API key; the
   extension's key; a report's) — one key per intent, kept across a retry and a double press; what each 409 says
   (`CLOSURE_ALREADY_EXTENDED`, `CLOSURE_EXTENDED`, `ANNOUNCEMENT_NOT_STARTED`, `REPORT_ALREADY_DECIDED`,
   `FAVORITES_LIMIT_REACHED`, the void's).
10. **Roles:** what the owner, reception, the admin and a signed-in user each see and may press — **always backed by
    the server** (a 403 handled); a guest pressing the favourite or the report action (the sign-in with its reason,
    the account decisions).
11. **The navigation:** the pages' routes and their places in the dashboard's grouped navigation (P3) for each role,
    and the account's links (P4).
12. **Each width's layout** against foundation §9, each state, and accessibility (names, landmarks, focus after each
    dialog and sheet; the menu-item focus lesson of #122 and #124).
13. **Design issues** found in the reading — numbered, each with its report and fix, **built only once the owner
    approves** (as `WORKER_A\DESK_SCREENS\2_PLAN.md` §8); anything that would change a settled decision → a
    *Proposed alternative*.
14. **Any document this proves wrong** — as a proposal, never applied silently.

**The decisions are proposals you may challenge** (the owner's rule): where you see a better way, argue it with
evidence from the code or the documents in *Proposed alternatives*, with its cost — never apply it.

## 3. Read first

`CLAUDE.md`; `docs/development/workflow.md`; `testing.md`; `docs/frontend/architecture.md` (§1–§3, §5, §7);
`design-system/foundation.md` (§9 widths, §10 actions and accessibility, §12 components, §13 the screens, §15 touch);
`localisation.md`; `documentation.md` §5; `docs/features/payments.md`, `announcements.md`, `data-reports.md`,
`favorites.md`, `directory.md`, `desk.md`, `subscriptions.md`, `auth.md`; `docs/api/api-contract.md` (§1–6, *Front
desk (managed)* — the payments list and the void —, *Announcements (managed)* with the extension, *Data reports*,
*Favourites*, the directory's space page, the error codes); ADR 0002, 0009, 0010, 0015; `docs/plans/v1-mvp.md` steps
9–10; `docs/design/SCREENS.md` (screens 10, 11, 17, 18, 23, 28 and the space page); the prototypes named in §2 and the
shared modules they use; `C:\dev\masaha\workspace\DESIGN\DECISIONS\` (`DECISIONS_DESK.md`, `DECISIONS_OWNER.md`,
`DECISIONS_ADMIN.md`, `DECISIONS_ACCOUNT.md`, `DECISIONS_PUBLIC.md`, `DECISIONS_SHARED.md`); the round-2 reviews that
cover these screens, where they exist — `C:\dev\masaha\workspace\DESIGN\ROUND2\REPORT\R2-OW-*`, `R2-AD-*`, `R2-AU-*`,
`R2-PU-*`, `R2-DK-*` (read only the issues about these screens; do not copy a defect they prove); `_SHARED\
OPEN_DECISIONS.md`; the findings index and findings 8, 87, 150, 162, 171; the code of `apps/web/src/pages/dashboard`
and `pages/site` (the shells, routes, navigation per role, the space page), `features/desk` (payments it already
shows), `features/directory` (the cards), `shared/routing`, `shared/session`, `shared/forms`, `shared/lists`,
`shared/copy`, `shared/api`, the design system's components; `packages/shared`'s `payments`, `announcements`,
`data-reports`, `favorites`, `directory` exports; `apps/web/scripts/` (`check:build`'s rules: the dashboard's code
stays out of the site's first download); `WORKER_A\DESK_SCREENS\2_PLAN.md` as the model of a web plan.

## 4. The plan's shape

As `WORKER_A\DESK_SCREENS\2_PLAN.md`: a header (base sha, worker, folder, the PRs with their branch, size and title);
summary; the contract per PR (scope, acceptance criteria, out of scope); the reading done and what it changed; the
decisions as built; stronger decisions (S…) and **Proposed alternatives**; related findings (folded or not, why);
design issues (each with its fix, built only once the owner approves); the files; the interfaces and the words; the
tests with their breaks; each PR's review focus; the commits; the procedure and the executor's rules; the decisions
needed from the owner (each with options and a recommendation). Stop after saving it, and reply only `PLAN READY:
C:\dev\masaha\workspace\WORKER_A\PAYMENTS_STEP10\2_PLAN.md` with the PR count and the number of decisions for the
owner.
