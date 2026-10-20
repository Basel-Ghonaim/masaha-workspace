# DESK PR 4 — collecting a visit's debt, and writing one off (K6, DK-012), the API — PLAN ONLY

**No branch, no checkout, no file edit in the repository, no commit, no install, no test run, no
server, no database command.** You write one file — the plan — then stop.
**No trial build anywhere either:** no temporary copy of the repository, no `git worktree add`, no
`git stash`, no scratch or temp folder holding code, no `node` / `tsx` / `tsc` / `vitest` / `psql` /
`npm` run — not in the repository, not in a scratchpad, not in a temp directory. The only commands are
`git fetch`, `git show`, `git log`, `git ls-tree`, `git grep`, `git diff` between commits, read-only `gh`,
and reading files. Where you are unsure that something works, write it in the plan as **a check the
executor makes first, with what to do if it fails** — never try it yourself. Read only the files the plan
needs, each once.

**The task's folder:** `C:\dev\masaha\workspace\WORKER_B\DESK\`. This prompt is `1_PLAN_PROMPT_PR4.md`;
**save the plan as `2_PLAN_PR4.md` here**; the report will be `4_REPORT_PR4.md`. If you are Claude Code: use
`write-plan` for its discipline (save the file; no plan-mode step is needed).

**Where you read.** `C:\dev\masaha\app-b` (worker B's worktree) — commit objects only: `git fetch origin`,
then `git show <ref>:<path>`, `git ls-tree`, `git grep <ref>`. Never check anything out. Worker A builds
OWNER_SETUP (`apps/web`, `docs`) in `C:\dev\masaha\app` — never work there.

## 0. The base and what runs beside it

> **Update 2026-10-20:** #97 **merged** at `abc28e73`; its branch is deleted. Plan from `origin/main`
> (it holds `e122b95d`); read PR 3's code there. **`0_CARRIED_FROM_97.md` exists** — read it: its items
> are this PR's first commit(s), item 2 decided by the owner as (b).

Plan from **`origin/main` plus DESK PR 3**, `feat/auto-checkout` at **`e122b95d`** (#97: pushed, green,
under review, not merged). PR 3 brings what this PR builds on: `payments`' `balance.ts` and the uncollected
visits read, `visits`' pricing of an unpriced visit, the codes `VISIT_ALREADY_PRICED` and
`VISIT_ALREADY_CLOSED`. Read them on `origin/feat/auto-checkout`. **The executor starts only after #97 has
merged;** its first step is `git diff --name-status e122b95d origin/main` — a code file the plan names changed
in a way the plan does not cover → stop and ask. If `0_CARRIED_FROM_97.md` exists in this folder when the
executor starts (small fixes from #97's review, the owner's rule), its items are **this PR's first commit**;
the plan says so, without guessing its content.

Worker A's OWNER_SETUP runs in parallel (`apps/web`, `docs`): name any shared document you edit (the findings
index, `overview.md`, `v1-mvp.md`) as a likely text conflict. **Finding numbers:** this PR's start at **110**
(worker A's run from 101; 98 and 100 are worker B's) — write `110`, `111`, … in the plan.

## 1. The plan must stand alone

A fresh Claude Code conversation executes the PR, and another Claude Code conversation reviews it (one
reviewer, no subagents). Every decision with its one-line reason; the files; each route, schema, service
function, transaction and type with its interface; each test with its lane, title and the break that must
make it fail (`docs/development/testing.md` §3 — **every break run and its red output recorded**); **each
permission, each money rule, each idempotency key and each race gets a deliberate break**; the commits,
subjects counted (≤ 50); fixes before the push folded (`--fixup` + autosquash, `GIT_SEQUENCE_EDITOR=:`); every
new decision and history line ends with its date and `#PRNUM`; the procedure with its commands (the branch
`feat/visit-debts` from the latest `origin/main` in `C:\dev\masaha\app-b`, `--no-track`; `masaha_b_dev` /
`masaha_b_test`; `docker start masaha-postgres-1`, never `db:up`, never `npm ci`; **memory: one full test run
at a time on this machine, none while a `vitest` of `C:\dev\masaha\app\` runs, the free memory recorded
before each full lane, a lane killed for memory stops the work**; per commit `lint` + `typecheck`; on the
head once `test:unit`, `test:api`, `format:check`, `check:links`, and `npm run build -w @masaha/shared` if the
shared package changes; **the schema change:** a migration by `migrate dev --create-only` run **once** — then
the executor checks the folder; on data loss Prisma refuses: use `migrate diff --script` — and both B
databases migrated; a real run on 3321; push; `gh pr create --assignee @me --label feat --label area:api
--label area:docs` (`area:web` too if the catalogues change); `gh pr checks` and `CLEAN`; the conflict check);
a **"Stop and ask"** list; the executor's stop rule (**a test it cannot run stops the work** — the same wording
as `3_EXEC_PROMPT_PR3.md` §2 in this folder, its break clause included); the executor's scripts kept in this
folder's `scripts\`, never committed; an appendix mapping steps to Claude's skills, "only a map". Never merge;
no tool attribution; stage by path.

## 2. The owner's decisions (2026-10-20)

**The goal:** the desk collects a closed visit's unpaid charge, or records it as a customer's debt by phone,
and the owner writes off a debt that will not be collected — the API only; the desk's screen (its «غير
محصّلة» tab) is worker A's later item. Source: `2_PLAN.md`'s alternative **A3** (taken by the owner), the
desk decisions **K6** and **DK-012** (`C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_DESK.md`), the
data model's *Front desk and money*.

1. **One PR**, ≈ 30 files, one migration; no split.
2. **The payment route is the build map's general one, not a visit-scoped route** (A3's
   `POST …/visits/:visitId/payments` is replaced): `POST /manage/spaces/:spaceId/payments` (🧾, staff), its
   body naming the item paid — a visit now; step 8 adds a subscription to the same route — with the
   `Idempotency-Key` (ADR 0015), on a **closed, priced** visit, never above the balance
   (`PAYMENT_EXCEEDS_DUE`), the payment recorded with who took it. Any part left unpaid follows the data
   model's *Unpaid visit* rule: a phone is required, which attaches the space's customer (created if new) —
   unless the visit already has one.
3. **«تسجيل دينًا» (DK-012):** an uncollected visit with no customer becomes a customer's debt by a phone
   **with no payment** — the same route with no amount, or its own small route if the contract reads better;
   say which and why.
4. **Write-off (K6), owner only (🏢):** on **any closed visit with a balance above zero** — an uncollected
   visit or a customer's unpaid visit; a partly paid visit has its **remainder** written off and its payments
   stay. A **required reason**; recorded (who, when, why) and audited; never a payment, never a deletion. An
   **unpriced** visit cannot be written off — it is priced first (PR 3's pricing route); refuse it with the
   existing `VISIT_NOT_PRICED` or a code of its own, say which.
5. **Undoing a write-off, owner only:** reversible, audited (who, when; the original write-off kept in the
   audit). **A payment on a written-off visit is refused** with a code that tells the desk to have the owner
   undo the write-off first — cash is never taken unrecorded.
6. **What a write-off changes:** the visit leaves the uncollected visits and the customer's debt; the data
   model's *Uncollected visits* and *Customer debt* lines say "not written off".
7. **Documents:** the contract (the payment route, the write-off and its undo, the new codes with their
   Arabic and English lines — the Arabic needs the owner's approval, listed in the PR's description);
   `payments.md`, `visits.md`, `desk.md`; the data model; `security.md` if a new permission; **the build map's
   step 9 line** keeps only voids, collections per staff member and finance (this PR takes receiving a
   visit's payment); `overview.md`.
8. **Not here:** the shared desk device (an idle sign-out, «تبديل الموظف» — the owner moved it to the desk's
   screen item); voids and collections (step 9); subscriptions' payments (step 8); any web screen.

## 3. Read first

`CLAUDE.md`; `docs/development/workflow.md`; `testing.md`; `docs/backend/conventions.md`; `security.md`;
ADR 0009, 0010, 0015; `docs/architecture/data-model.md` (*Front desk and money*); `docs/api/api-contract.md`
(§1–4, *Front desk (managed)*, payments); `docs/features/payments.md`, `visits.md`, `desk.md`;
`docs/plans/v1-mvp.md` steps 7–9 and its route table; `C:\dev\masaha\workspace\WORKER_B\DESK\2_PLAN.md`
(its approval note, alternative A3, §12's procedure as a model) and `4_REPORT_PR3.md`; the code of `payments`,
`visits`, `desk`, `customers` and `shared/auth` on `origin/feat/auto-checkout`; `schema.prisma` and the last
migrations; the desk prototype's debt and uncollected parts (`docs/design/prototype/masaha/desk-*`) only
where the API's shape depends on them.

## 4. Decisions the plan must state (with a recommendation each)

- The route shapes (the payment's item; «تسجيل دينًا»; the write-off and its undo), and their responses.
- The schema: the write-off's columns and constraints (together, non-blank reason, only on a closed visit),
  and how an undo is stored (cleared columns, the history in the audit).
- The new codes, the locks and the order of checks under the space's lock, each race (two desks collecting
  the same visit; a payment against a write-off at the same moment).
- Anything in the documents that this decision set proves wrong — as a proposal, never applied silently.

## 5. The plan's shape

As `2_PLAN.md`: summary; the contract (scope, acceptance criteria, out of scope); the reading done and what
it changed; the decisions as built; stronger decisions (S…) and **Proposed alternatives** (the owner may
prefer them); related findings (folded or not, why); the files; the interfaces; the tests with their breaks;
the commits; the procedure and the stop rules; the decisions needed from the owner. Stop after saving it.
