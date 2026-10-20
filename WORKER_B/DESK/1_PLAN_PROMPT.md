# DESK — the front desk and visits, the API (build map step 7) — PLAN ONLY

**No branch, no checkout, no file edit in the repository, no commit, no install, no test run, no
server, no database command.** You write one file — the plan — then stop.
**No trial build anywhere either:** no temporary copy of the repository, no `git worktree add`, no
`git stash`, no scratch or temp folder holding code, no `node` / `tsx` / `tsc` / `vitest` / `psql` /
`npm` run — not in the repository, not in a scratchpad, not in a temp directory. The only commands are
`git fetch`, `git show`, `git log`, `git ls-tree`, `git grep`, `git diff` between commits, read-only `gh`,
and reading files. Where you are unsure that something works, write it in the plan as **a check the
executor makes first, with what to do if it fails** — never try it yourself. Read only the files the plan
needs, each once.

**The task's folder:** `C:\dev\masaha\workspace\WORKER_B\DESK\`. This prompt is `1_PLAN_PROMPT.md`; **save
the plan as `2_PLAN.md` here**; reports `4_REPORT_PR<n>.md`. If you are Claude Code: use `write-plan` for its
discipline (save the file; no plan-mode step is needed).

**Where you read.** `C:\dev\masaha\app-b` (worker B's worktree) — commit objects only: `git fetch origin`,
then `git show origin/main:<path>`, `git ls-tree`, `git grep origin/main`. Never check anything out. Worker A
builds USERS (`apps/web`, `docs`) in `C:\dev\masaha\app` — never work there.

## 0. The base and what runs beside it

Plan from today's `origin/main`, **which holds SETTINGS (#92)**: the space's settings and capacity routes,
the `occupancy` module (capacity only), `receptionMayTypePrices`, DI-41 and "a change applies from then on" in
the data model. Worker A's USERS (`feat/admin-users`, web and docs) runs in parallel: name any shared
document you edit (the findings index, `overview.md`, `architecture.md`) as a likely text conflict. The
executor's first step for each PR: `git diff --name-status <the plan's base> origin/main`; a code file the
plan names changed in a way the plan does not cover → stop and ask. **Finding numbers:** the next free ones
on the latest index (USERS may take some) — write `<n>` in the plan.

## 1. The plan must stand alone

A fresh Claude Code conversation executes each PR, and another Claude Code conversation reviews it (split
across two subagents when a PR is large). Every decision with its one-line reason; the files; each route,
schema, service function, transaction and type with its interface; each test with its lane, title and the
break that must make it fail (`docs/development/testing.md` §3 — **every break run and its red output
recorded**); **each permission, each money rule, each idempotency key and each race gets a deliberate
break**; the commits, subjects counted (≤ 50); fixes before the push folded (`--fixup` + autosquash,
`GIT_SEQUENCE_EDITOR=:`); every new decision and history line ends with its date and `#PRNUM`; the
procedure with its commands (branches from the latest `origin/main` in `C:\dev\masaha\app-b`, `--no-track`;
`masaha_b_dev` / `masaha_b_test`; `docker start masaha-postgres-1`, never `db:up`, never `npm ci`; one full
test run at a time on this machine; per commit `lint` + `typecheck`; on the head once `test:unit`,
`test:api`, `format:check`, `check:links`, and `npm run build -w @masaha/shared` if the shared package
changes; **each schema change**: a migration by `migrate dev --create-only` run **once** — then the executor
checks the folder; on data loss Prisma refuses: use `migrate diff --script` — and both B databases migrated;
a real run on 3321; push; `gh pr create --assignee @me --label feat --label area:api --label area:docs`;
`gh pr checks` and `CLEAN`; the conflict check); a **"Stop and ask"** list; the executor's stop rule (**a test
it cannot run stops the work** — the same wording as `C:\dev\masaha\workspace\WORKER_B\SETTINGS\3_EXEC_PROMPT.md`
§2, its break clause included); an appendix mapping steps to Claude's skills, "only a map". Never merge; no
tool attribution; stage by path.

## 2. The owner's decisions (2026-10-19)

**The goal (build map step 7):** the staff run the day at the desk — check in and out, the visit charge and
its payment at check-out, live status with the manual override, auto check-out, uncollected visits. The API
only; the desk screen (13) is worker A's later item.

1. **One plan, three PRs in sequence** (each cut from `main` once the one before it has merged):
   - **PR 1 — presence and live status:** `occupancy`'s single definition of *present* (open visits plus
     open subscription check-ins), the count and the one list of who is present, the pure live-status rule
     (ADR 0008), the manual override, the full warning's input; the public directory's live state where
     step 7 brings it (build map *Ordering notes*: "until the front desk, Home, the directory and the space
     page show no live state").
   - **PR 2 — the visit:** `desk`'s check-in and check-out of a visit, each in one transaction; the charge
     (data model *Visit charge*: rates copied at check-in, rounding and the cap read at check-out, DI-41's
     fallbacks, the student audience only where it changes a rate); the payment at check-out — **the first
     payment written** (closes finding 15, ADR 0010, ADR 0015's idempotency); a hand-typed price under
     `receptionMayTypePrices` with its **required reason** (`OPEN_DECISIONS.md` point 1, settled in #92); an
     unpaid visit only with a phone number.
   - **PR 3 — auto check-out and uncollected visits:** the scheduler port's job, the uncollected visits read
     (`payments`, conventions §9), and **Q4 (settled):** with the switch off and no rate at all, reception
     closes the visit **unpriced**, and it appears for the owner to price (the owner's «يحتاج انتباهك»
     reads it later — say what this PR exposes for it) — never closed free.
   If the reading shows a better cut, propose it in *Proposed alternatives* — do not apply it.
2. **The scheduler (ADR 0014):** the job runs through an internal, secret-protected endpoint that a **free
   external cron service calls every 5 minutes** (not GitHub Actions' schedule: too imprecise). The job is
   idempotent and catches up. **A stay closed automatically is closed at its due time** — the closing time or
   the end of the stay limit — **never at the run's time**, so the visitor never pays for the scheduler's
   delay. Name the env var for the secret, the endpoint, its auth, its rate and its logging; say what the
   deployment documents must gain (the owner sets up the cron service by hand — a short runbook line).
3. **The manual override of the live status** ends by itself at the space's next closing, or earlier when
   staff clear it. No override outlives its day.
4. **The shared desk device** (`OPEN_DECISIONS.md` point 4) is **not** settled here — it waits for step 9
   (payments). Do not build an idle sign-out or a staff switch.
5. **The unpaid visit's customer:** the minimum only — a customer found or created by the phone number (the
   name if given), the visit's charge counted in that customer's debt. The customers list, the file and
   subscriptions are step 8.
6. **Claude Code throughout.**

**Your right to challenge (the owner's rule):** the decisions above, and any fixed rule you meet in the
documents (an ADR, a convention, a design decision), are proposals you may challenge. If you see a better
solution, **build the plan on the decision as given**, and put your alternative in a section **"Proposed
alternatives"** — what, why, its cost, and what changes in the plan if the owner takes it. Never apply an
alternative yourself.

## 3. Read first (from `origin/main`)

`CLAUDE.md`; `docs/development/workflow.md`; `docs/development/testing.md`; `docs/backend/conventions.md`
(§6 audit, §7–§8 modules and rules, §9 *the front desk*, *occupancy*, *composed reads*, *settings*, §11 time,
§13 idempotency and concurrency, the ledger's rules); `docs/backend/security.md`; `docs/api/api-contract.md`
(the managed routes, the planned surface); `docs/architecture/data-model.md` (visits, check-ins, payments,
customers, `SpaceOccupancy`, *Visit charge*, *Front desk and money*, derived values); ADR 0002, 0008, 0009,
0010, 0012, 0014, 0015; `docs/plans/v1-mvp.md` (step 7, ordering notes, planned API surface);
`docs/features/` (`spaces.md`, `space-settings.md`, `occupancy.md`, `directory.md`, `packages.md`);
`docs/design/SCREENS.md` (13) and `C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_DESK.md` (and
`DECISIONS_OWNER.md` O3 for the work queue); `C:\dev\masaha\workspace\_SHARED\OPEN_DECISIONS.md`; findings 15,
17, 23, 52; `apps/api/prisma/schema.prisma` (the desk's tables); the code of `occupancy`, `space-settings`,
`spaces` (the lock, hours), `packages`, `directory`, `space-links` (the latest patterns: routes, `requireCan`,
validation, audit, the race tests), `shared/auth`, `shared/rate-limit`, the clock and any scheduler port.

## 4. Boundaries

`apps/api`, `packages/shared`, `docs`. Nothing in `apps/web`. Schema changes where the tables lack what the
decisions need — each named with its reason. No dependency without "Decisions needed". New error codes
follow `add-error-code`'s rules, each listed in "Decisions needed" with its Arabic and English lines.
