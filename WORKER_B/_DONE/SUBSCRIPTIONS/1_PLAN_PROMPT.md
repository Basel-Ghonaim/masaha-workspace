# SUBSCRIPTIONS — customers, subscriptions and subscription check-ins, the API (build map step 8) — PLAN ONLY

**No branch, no checkout, no file edit in the repository, no commit, no install, no test run, no
server, no database command.** You write one file — the plan — then stop.
**No trial build anywhere either:** no temporary copy of the repository, no `git worktree add`, no
`git stash`, no scratch or temp folder holding code, no `node` / `tsx` / `tsc` / `vitest` / `psql` /
`npm` run — not in the repository, not in a scratchpad, not in a temp directory. The only commands are
`git fetch`, `git show`, `git log`, `git ls-tree`, `git grep`, `git diff` between commits, read-only `gh`,
and reading files. Where you are unsure that something works, write it in the plan as **a check the
executor makes first, with what to do if it fails** — never try it yourself. Read only the files the plan
needs, each once.

**The task's folder:** `C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\`. This prompt is `1_PLAN_PROMPT.md`;
**save the plan as `2_PLAN.md` here**; reports `4_REPORT_PR<n>.md`. If you are Claude Code: use `write-plan`
for its discipline (save the file; no plan-mode step is needed).

**Where you read.** `C:\dev\masaha\app-design` (the read-only worktree the reviews use; worker B's DESK
PR 4 executes in `C:\dev\masaha\app-b` meanwhile — never work there) — commit objects only: `git fetch
origin`, then `git show origin/main:<path>`, `git ls-tree`, `git grep origin/main`. Never check anything out. Worker A builds OWNER_SETUP (`apps/web`, `docs`) in
`C:\dev\masaha\app` — never work there.

## 0. The base and what runs before it

Plan from today's `origin/main` (DESK PRs 1–3 merged: #94, #95, #97). **DESK PR 4** (`feat/visit-debts`) is
planned, not built: `C:\dev\masaha\workspace\WORKER_B\DESK\2_PLAN_PR4.md` — read its D1–D4 and S1–S5: it
builds the general `POST /manage/spaces/:spaceId/payments` (`visitId` in the body, in `desk`, the ledger's
trigger rules), which **this item's PR 2 extends with `subscriptionId`** ("exactly one of"). **This item's
executor starts only after DESK PR 4 has merged**; its first step is `git diff --name-status <the plan's
base> origin/main`, and it re-reads DESK PR 4's merged payment route against the plan — a difference the plan
does not cover → stop and ask. Worker A's OWNER_SETUP runs in parallel (`apps/web`, `docs`): name each shared
document you edit as a likely text conflict. **Finding numbers:** this item's start at **120** (worker A's
run from 101; DESK PR 4 holds 110–119) — write `120`, `121`, … in the plan.

## 1. The plan must stand alone

Fresh Claude Code conversations execute each PR, and another Claude Code conversation reviews each (one
reviewer, no subagents). Every decision with its one-line reason; the files; each route, schema, service
function, transaction and type with its interface; each test with its lane, title and the break that must
make it fail (`docs/development/testing.md` §3 — **every break run and its red output recorded**); **each
permission, each money rule, each idempotency key and each race gets a deliberate break**; the commits,
subjects counted (≤ 50); fixes before the push folded (`--fixup` + autosquash, `GIT_SEQUENCE_EDITOR=:`); every
new decision and history line ends with its date and `#PRNUM`; the procedure with its commands (branches from
the latest `origin/main` in `C:\dev\masaha\app-b`, `--no-track`; `masaha_b_dev` / `masaha_b_test`;
`docker start masaha-postgres-1`, never `db:up`, never `npm ci`; **memory: one full test run at a time on
this machine, none while a `vitest` of `C:\dev\masaha\app\` runs, the free memory recorded before each full
lane, a lane killed for memory stops the work**; per commit `lint` + `typecheck`; on the head once
`test:unit`, `test:api`, `format:check`, `check:links`, and `npm run build -w @masaha/shared` if the shared
package changes; **each schema change**: a migration by `migrate dev --create-only` run **once** — then the
executor checks the folder; on data loss Prisma refuses: use `migrate diff --script` — and both B databases
migrated; a real run on 3321; push; `gh pr create --assignee @me --label feat --label area:api --label
area:docs` (`area:web` if the catalogues change); `gh pr checks` and `CLEAN`; the conflict check); a **"Stop
and ask"** list; the executor's stop rule (**a test it cannot run stops the work** — the same wording as
`C:\dev\masaha\workspace\WORKER_B\DESK\3_EXEC_PROMPT_PR3.md` §2, its break clause included); the executor's
scripts kept in this folder's `scripts\`, never committed; **carried items:** if a `0_CARRIED_FROM_<n>.md`
naming one of these PRs exists when its executor starts (small fixes from the previous PR's review, the
owner's rule), its items are that PR's first commit; an appendix mapping steps to Claude's skills, "only a
map". Never merge; no tool attribution; stage by path.

## 2. The owner's decisions (2026-10-20)

**The goal (build map step 8):** the staff keep customers on file and run their subscriptions — limits,
billing, progress, statement, renewal, ending early — and subscription check-ins. The API only; the screens
(14, 15, 16) are worker A's later items. The tables `Customer`, `Subscription`, `CheckIn` exist since the
first migrations; `customers` and `subscriptions` modules exist in part (#95, #97) — read what they hold.

1. **Three PRs in sequence**, each cut from `main` once the one before it has merged:
   - **PR 1 — customers** (≈ 40 files): the list (paged, searched, filtered), create, the customer's file
     (subscriptions, balances, unpaid visits and their payments, the debt — K4), edit, archive and restore.
   - **PR 2 — subscriptions and their money** (≈ 50 files): a new subscription from a package or custom
     (the hand-typed price rule, #92), progress, status and statement, correcting one, ending early, a
     payment on a subscription through DESK PR 4's `POST …/payments` (`subscriptionId`), and the renewal
     with a debt (K3).
   - **PR 3 — subscription check-ins** (≈ 40 files): check-in with the limits' and the full space's
     warnings, check-out, the open and dated lists; the auto check-out already closes them (#97).
   If the reading shows a better cut, propose it in *Proposed alternatives* — do not apply it.
2. **Two active subscriptions for one customer are allowed;** a check-in names its subscription, and the
   desk may preselect when the customer holds only one active.
3. **A renewal's start date:** the server proposes the day after the current subscription's end when it is
   still running, else today; the desk may change it.
4. **Correcting a subscription:** its limits and dates by the staff; its price and billing by the **owner
   only**, with a required reason (the hand-typed price rule, extended); every correction audited.
5. **Ending early changes the status only:** no refund and no proration; the balance stays; any money
   correction is a void (step 9).
6. **The customers list's payment filter and debts are computed in the database** (an aggregate query owned
   by the module that owns the balance), never by reading every row into memory — #97's review (finding on
   the uncollected read's growth) is the reason.
7. **Phone privacy (`C:\dev\masaha\workspace\_SHARED\OPEN_DECISIONS.md` point 3, settled now):** a paged,
   searched list for both roles; **no export for anyone** in step 8 (an export is the owner's, later, in
   finance). Update that file's point 3 in the PR's report (the supervisor commits nothing there).
8. **The renewal with a debt (K3) is one request:** the renewal route takes an optional amount, which the
   **server** allocates oldest debt first, one payment per item, in one transaction under one
   `Idempotency-Key` — not the client. The build map's route row ("warns when the customer has a balance")
   is updated to say so.
9. **Subscription check-ins live in `desk`,** beside the visits' check-in and check-out (the same lock, the
   same order of checks, the same full-space warning); the build map's `/check-ins` rows are kept as paths.
10. **One definition of *present*:** the PR that first touches it (PR 3) makes it one helper in `occupancy`
    used by the read, the warnings and the directory (#95's review nit 7; its finding, recorded by DESK PR 4,
    resolves here).

**Unchanged (settled):** editing a customer, both roles; archiving and restoring, the owner (ADR 0009, as
revised); an owing customer may be archived after a confirm (DK-014); limits warn, never block; the status
from the end date or the total, whichever comes first; a hand-typed price needs a reason; no merging of
duplicate customers in v1; "Settles: date inputs" is the web's.

## 3. Read first

`CLAUDE.md`; `docs/development/workflow.md`; `testing.md`; `docs/backend/conventions.md` (§5, §9, §13);
`security.md`; ADR 0009, 0010, 0015; `docs/architecture/data-model.md` (the entities, *Front desk and money*,
*Subscription scenarios*, the constraints); `docs/api/api-contract.md` (§1–4, *Front desk (managed)*,
payments); `docs/features/payments.md`, `visits.md`, `desk.md`, `occupancy.md`, `packages.md`,
`space-settings.md`; `docs/plans/v1-mvp.md` steps 7–9 and the route table; the desk design decisions
`C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (K1, K3, K4, K5, DK-005, DK-007, DK-008,
DK-010, DK-013, DK-014, DK-020, DK-022, DK-023); `OPEN_DECISIONS.md`; DESK's `2_PLAN.md` (its §12 procedure as
the model) and `2_PLAN_PR4.md`; the code of `customers`, `subscriptions`, `payments`, `visits`, `desk`,
`occupancy`, `packages`, `space-settings` and `shared/auth` on `origin/main`; `schema.prisma` and the
migrations that made the three tables; the demo seed; the desk prototype (`docs/design/prototype/masaha/
desk-*`) only where the API's shape depends on it.

## 4. Decisions the plan must state (with a recommendation each)

- Each route's shape and answer; the composed reads (the list, the file, the statement) and their bounds
  (api-contract §4).
- The status and progress rules in code (Gaza dates, Saturday to Friday weeks), and where each lives.
- The idempotency keys (ADR 0015: subscriptions and customers gain theirs), the locks, the order of checks,
  each race (two desks renewing one customer; a check-in racing a correction or an end).
- Any migration (indexes, `CHECK`s, the correction's reason), and any document this decision set proves
  wrong — as a proposal, never applied silently.

## 5. The plan's shape

As DESK's `2_PLAN.md`: summary; the contract per PR (scope, acceptance criteria, out of scope); the reading
done and what it changed; the decisions as built; stronger decisions (S…) and **Proposed alternatives**;
related findings (folded or not, why); the files; the interfaces; the tests with their breaks; the commits;
the procedure and the stop rules; the decisions needed from the owner. Stop after saving it.
