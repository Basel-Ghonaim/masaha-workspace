# PAYMENTS — payments voided, the payments list and «دفعاتي اليوم», on the API (build map step 9) — PLAN ONLY

**No branch, no checkout, no file edit in the repository, no commit, no install, no test run, no
server, no database command.** You write one file — the plan — then stop.
**No trial build anywhere either:** no temporary copy of the repository, no `git worktree add`, no
`git stash`, no scratch or temp folder holding code, no `node` / `tsx` / `tsc` / `vitest` / `psql` /
`npm` run — not in the repository, not in a scratchpad, not in a temp directory. The only commands are
`git fetch`, `git show`, `git log`, `git ls-tree`, `git grep`, `git diff` between commits, read-only `gh`,
and reading files. Where you are unsure that something works, write it in the plan as **a check the
executor makes first, with what to do if it fails** — never try it yourself. Read only the files the plan
needs, each once.

**This is a planning task, not a Work Item's start:** do not run `start-work-item` (it cuts a branch) and do
not stop on the worktree being detached. If you are Claude Code: use `write-plan` for its discipline only
(save the file; no plan-mode step is needed).

**The task's folder:** `C:\dev\masaha\workspace\WORKER_B\PAYMENTS\`. This prompt is `1_PLAN_PROMPT.md`; **save
the plan as `2_PLAN.md` here**; reports `4_REPORT_PR<n>.md`.

**Where you read.** `C:\dev\masaha\app-design` — commit objects only: `git fetch origin`, then `git show
origin/main:<path>`, `git ls-tree`, `git grep origin/main`. Never check anything out, switch or reset it: a
small task (`chore/conflict-guard`) may hold a branch there, and a planner and reviewers read there too. If a
`git` command fails on a `.lock` file, wait 30 s and retry once. Worker A's `C:\dev\masaha\app` and worker B's
`C:\dev\masaha\app-b` — never work there.

## 0. The base and what runs beside it

Plan from today's `origin/main` (write its sha in the plan's header; #112, ANNOUNCEMENTS PR 1, merged
2026-10-24). **Beside it:**
- **Worker A** plans DESK_SCREENS (screens 13–16; `WORKER_A\DESK_SCREENS\1_PLAN_PROMPT.md`), whose plan will
  hand worker B up to three short API specs (an allocation preview, the statement read in one snapshot,
  reception's idle sign-out on the server). **They are not this item's:** do not plan them; name any route of
  this item they would touch so the two do not collide.
- **`TASKS\CONFLICT_GUARD_BASEL`** (CI, `package.json`, `apps/api/scripts/`, the findings index, a few
  documents) and later **`TASKS\DEMO_DAILY_BASEL`** (the demo seed): name each file you share as a likely text
  conflict.
- **ANNOUNCEMENTS PRs 2–4** follow this item (`WORKER_B\ANNOUNCEMENTS\2_PLAN.md`, approved): name any file both
  touch.
- **Finding numbers:** this item's start at **170** — write `170`, `171`, … in the plan.

## 1. The plan must stand alone

Fresh Claude Code conversations execute each PR, and another Claude Code conversation reviews each (one
reviewer, no subagents). Every decision with its one-line reason; the files; each route, schema, service
function, transaction and type with its interface; each new error code (through the `add-error-code` skill's
steps, written so an executor without that skill follows them); each test with its lane, title and the break
that must make it fail (`docs/development/testing.md` §3 — **every break run and its red output recorded**);
**each permission (owner, reception, admin, another space's staff), each money rule, each idempotency key and
each race gets a deliberate break**; the commits, subjects counted (≤ 50); fixes before the push folded
(`--fixup` + autosquash, `GIT_SEQUENCE_EDITOR=:`); every new decision and history line ends with its date and
`#PRNUM`; the procedure with its commands — as `WORKER_B\ANNOUNCEMENTS\2_PLAN.md` §12 has them (branches from
the latest `origin/main` in `C:\dev\masaha\app-b`, `--no-track`; `masaha_b_dev` / `masaha_b_test`; `docker
start masaha-postgres-1`, never `db:up`, never `npm ci`; **memory: one full test run at a time on this
machine, none while a `vitest` of `C:\dev\masaha\app\` runs, the free memory recorded before each full lane; a
full lane killed for low memory is re-run once when the machine is quieter, killed again → carry on and CI's
run of that lane on the pushed head judges (red → stop)**; per commit `lint` + `typecheck`; on the head once
`test:unit`, `test:api`, `format:check`, `check:links`, and `npm run build -w @masaha/shared` if the shared
package changes; **each schema change**: a migration by `migrate dev --create-only` run **once** — then the
executor checks the folder; non-interactive or on data loss: `migrate diff --script` — and both B databases
migrated; a real run on 3321 with the demo data, a self-judging script (`PASS|FAIL`, `ALL PASS`) (**a demo
account or data that does not hold what a real-run case needs → stop and report; never change data through
the app to get past it**; the run's own writes named); `#PRNUM` replaced per commit tree by a self-checking
script (`WORKER_B\SUBSCRIPTIONS\scripts\prnum-fix109.sh` the model); push; `gh pr create --assignee @me
--label feat --label area:api --label area:docs` (`area:web` if the catalogues change); `gh pr checks` and
`CLEAN`; the conflict check); a **"Stop and ask"** list; the executor's stop rule (**a test it cannot run stops
the work** — the wording of `WORKER_B\ANNOUNCEMENTS\3_EXEC_PROMPT_PR1.md` §3, its break clause included);
**never leave silently:** an executor that would leave a carried item or a review nit undone stops and asks;
fix rounds run only what the change touches; the executor's scripts in this folder's `scripts\`, never
committed; an appendix mapping steps to Claude's skills, "only a map". Never merge; no tool attribution; stage
by path.

**Carried items — this item's PR 1 opens with them:** `C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\
0_CARRIED_FROM_112.md` (items 1–6, decided by the owner): its code fix (item 4, `start()` holding the 365-day
bound) with its test and break, and its document fixes, as PR 1's first commits before the plan's own, named in
the description under "Carried from #112". Plan them as commits (files, test, break); do not re-decide them.

## 2. The owner's decisions

**The goal (build map step 9, the API only):** payments are voided, and each staff member's collections are
seen — the owner's payments list with its filters and reception's «دفعاتي اليوم»; balances, credit and debts
are read where the desk already answers them (the customer's file, the statement, the uncollected visits) —
**read what is built** before adding anything. Recording a payment is built (#95, #100, #106). The screen (17,
`Payments.html`, `My payments.html`) is worker A's later item.

**Settled (ADR 0010, the build map, the design decisions):**
1. **Append-only:** a payment is never edited or deleted; a mistake is corrected by **voiding** it — **the owner
   only, with a reason**; the ledger keeps who recorded it, who voided it and when; **a voided payment counts
   nowhere** (ADR 0010 rules 3–5). Recording and voiding are audit entries, the owner's, never the admin's.
2. **The list** (`GET /manage/spaces/:spaceId/payments`, v1-mvp's route table): the owner sees all, with date,
   staff and method filters; **reception sees its own, today** (Gaza's day). «دفعاتي اليوم» shows a voided
   payment struck through (DECISIONS_DESK) — so voided ones are listed, marked.
3. **The void** (`POST …/payments/:paymentId/void`, 🏢, reason required).
4. No refunds, no credit across items, no editable payment (ADR 0010).

**For you to decide, with a recommendation each (the owner approves):**
5. **What a void changes downstream:** a visit's payment voided after its check-out (the visit owes again:
   uncollected, or its customer's debt?); a subscription's (its balance, its payment status, and a fixed one's
   price floor `PRICE_BELOW_PAID`); a payment whose item was written off since; the allocation of a renewal
   (rule 2) — say exactly what each read answers after a void, and that nothing else is rewritten.
6. **The void's idempotency and races:** a second void of the same payment (answered as it is, its first
   reason kept, as the write-off does — recommend); a void racing a new payment, a check-out, a write-off or a
   subscription's correction (the locks and their order, as D14 of SUBSCRIPTIONS and D13 of ANNOUNCEMENTS
   have them).
7. **The list's shape:** paging and bounds (api-contract §4), the date range's limit, the sort, the totals it
   answers (received, voided — by method?), what each row names (the item, the customer, who recorded it), and
   whether reception's «today» is a separate route or the same route narrowed by `can()`.
8. **The cut:** one PR or two (the void, then the list) — recommend, with the size.
9. **Any document this proves wrong** — as a proposal, never applied silently.

**The decisions are proposals you may challenge** (the owner's rule): where you see a better way, argue it
with evidence from the code or the documents in *Proposed alternatives*, with its cost — never apply it.

## 3. Read first

`CLAUDE.md`; `docs/development/workflow.md`; `testing.md`; `docs/backend/conventions.md` (§4–§9, the
front desk and composed reads, *the ledger's rules*, §11, §13); `security.md` (authorization); ADR 0009, 0010,
0015; `docs/architecture/data-model.md` (*Front desk and money*, the constraints, the derived values);
`docs/api/api-contract.md` (§1–6, *Front desk (managed)*, *Customers (managed)*, *Subscriptions (managed)*,
the error codes); `docs/features/payments.md`, `desk.md`, `visits.md`, `customers.md`, `subscriptions.md`;
`docs/plans/v1-mvp.md` step 9 and the route table; `C:\dev\masaha\workspace\DESIGN\DECISIONS\
DECISIONS_DESK.md` and `DECISIONS_OWNER.md` (the payments and void lines); `_SHARED\OPEN_DECISIONS.md`;
`WORKER_B\ANNOUNCEMENTS\0_CARRIED_FROM_112.md` and, for its items, `6_REVIEW_PR1_CLAUDE_CODE.md`; the code of
`payments`, `desk`, `visits`, `customers`, `subscriptions` and `shared/auth` (`can()`) on `origin/main`;
`schema.prisma` and the payments' migrations; the demo seed's payments; the prototype's `Payments.html` and
`My payments.html` only where the API's shape depends on them; `WORKER_B\ANNOUNCEMENTS\2_PLAN.md` as the model
of the plan.

## 4. The plan's shape

As `WORKER_B\ANNOUNCEMENTS\2_PLAN.md`: a header (base sha, worker, folder, the PRs with their branch, size and
title); summary; the contract per PR (scope, acceptance criteria, out of scope); the reading done and what it
changed; the decisions as built; stronger decisions (S…) and **Proposed alternatives**; related findings
(folded or not, why); the files; the interfaces; the tests with their breaks; the commits (the carried ones
first); the procedure and the stop rules; the decisions needed from the owner (each with options and a
recommendation). Stop after saving it, and reply only `PLAN READY:
C:\dev\masaha\workspace\WORKER_B\PAYMENTS\2_PLAN.md` with the PR count and the number of decisions for the
owner.
