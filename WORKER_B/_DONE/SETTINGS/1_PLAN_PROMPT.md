# SETTINGS — the space's operating settings and its capacity (the owner), DI-41 — PLAN ONLY

**No branch, no checkout, no file edit in the repository, no commit, no install, no test run, no
server, no database command.** You write one file — the plan — then stop.
**No trial build anywhere either:** no temporary copy of the repository, no `git worktree add`, no
`git stash`, no scratch or temp folder holding code, no `node` / `tsx` / `tsc` / `vitest` / `psql` /
`npm` run — not in the repository, not in a scratchpad, not in a temp directory. The only commands are
`git fetch`, `git show`, `git log`, `git ls-tree`, `git grep`, read-only `gh`, and reading files. Where you
are unsure that something works, write it in the plan as **a check the executor makes first, with what to
do if it fails** — never try it yourself. Read only the files the plan needs, each once.

**The task's folder:** `C:\dev\masaha\workspace\WORKER_B\SETTINGS\`. This prompt is `1_PLAN_PROMPT.md`;
**save the plan as `2_PLAN.md` here**; reports `4_REPORT_PR<n>.md`. If you are Claude Code: use
`write-plan` for its discipline.

**Where you read.** `C:\dev\masaha\app-b` (worker B's worktree, detached at `origin/main`) — read only commit
objects: `git fetch origin`, then `git show origin/main:<path>`, `git ls-tree`, `git grep`. Never check
anything out. Worker A builds OWNERS PR 3 (web) in `C:\dev\masaha\app` — never work there.

## 0. The base and what runs beside it

Plan from today's `origin/main` (`18ab1705` or later). Worker A's OWNERS PR 3 (`apps/web` and `docs` only)
runs in parallel; it touches `docs/features/space-links.md`, `docs/features/spaces.md`, the findings index,
`docs/frontend/architecture.md` and `docs/project/overview.md` — **a shared document edited here must be
named in the plan as a likely text conflict**. Findings 88–93 are taken: this item's numbers start at **94**
(worker A's PR 3 may take one — the executor checks the index on the latest `origin/main`). The executor's
first step: `git diff --name-status <the plan's base> origin/main`; a code file the plan names changed in a
way the plan does not cover → stop and ask.

## 1. The plan must stand alone

A fresh Claude Code conversation executes it, and another Claude Code conversation reviews it. Every
decision with its one-line reason; the files; each route, schema, service function and type with its
interface; each test with its lane, title and the break that must make it fail (`docs/development/testing.md`
§3 — **every break run and its red output recorded**); **each permission and each validation bound gets a
deliberate break**; the commits, subjects counted (≤ 50); fixes before the push folded (`--fixup` +
autosquash, `GIT_SEQUENCE_EDITOR=:`); every new decision and history line ends with its date and `#PRNUM`;
the procedure with its commands (the branch from the latest `origin/main` in `C:\dev\masaha\app-b`;
`masaha_b_dev` / `masaha_b_test`; `docker start masaha-postgres-1`, never `db:up`, never `npm ci`; one full
test run at a time on this machine; per commit `lint` + `typecheck`; on the head once `test:unit`,
`test:api`, `format:check`, `check:links`, and `npm run build -w @masaha/shared` if the shared package
changes; **if the schema changes**: a migration by `migrate dev --create-only` run **once** — then the
executor checks the folder; on data loss Prisma refuses: use `migrate diff --script` — and both B databases
migrated; a real run on 3321; push; `gh pr create --assignee @me --label feat --label area:api --label
area:docs`; `gh pr checks` and `CLEAN`; the conflict check); a **"Stop and ask"** list; the executor's stop
rule (**a test it cannot run stops the work** — the same wording as
`C:\dev\masaha\workspace\WORKER_B\_DONE\STAFF\3_EXEC_PROMPT.md` §2); an appendix mapping steps to Claude's
skills, "only a map". Never merge; no tool attribution; stage by path.

## 2. The owner's decisions (2026-10-19)

**Why this item now:** the front desk (step 7) reads these settings on every visit — auto check-out, the
stay limit, rounding, the day-price cap, student prices — and the full warning and the live status need the
capacity. The `space_settings` and `space_occupancy` tables exist; no route reads or writes them for the
owner. Design: `DECISIONS_OWNER.md` **O2** (capacity and the stay limit move to Settings, one card «الحضور
والحالة المباشرة»), OW-002, OW-021.

1. **Scope — every field of `SpaceSettings`, and the capacity:** auto check-out at closing, `maxStayMinutes`,
   the visit rounding rule and its minutes, the cap at the day price, student prices for visits, the WhatsApp
   reminder template — and the capacity (owned by `occupancy`, `space_occupancy`, created on its first write;
   conventions §9). A managed read and a managed write for each owning module (`space-settings`, and
   `occupancy` for the capacity — decide whether `occupancy` exists as a module yet, and if not, the
   smallest honest home that keeps conventions §9's ownership). Bounds for every number (the stay limit,
   the rounding minutes, the capacity) decided in the plan, each with its reason. The reminder template:
   its placeholders and their validation decided here, said in the contract; the finance step only reads it.
2. **Who edits — the owner only.** The permission table already says so (`space.settings.manage`,
   `space.capacity.manage`: owner; capacity is private from the admin, ADR 0002 and ADR 0008). Reception reads
   nothing here directly (the desk applies the values it needs). The admin does not edit a space's settings.
3. **DI-41 — a student visit where the space publishes no student hour or day price:** each missing student
   price falls back to the general one (as the desk prototype's `visitRates` does); the desk hides «طالب»
   where it changes nothing (the design's S1, unchanged). **Here only the documents:** the data model's
   *Visit charge* says it; the charge itself is built in step 7.
4. **Hand-typed prices at the desk (`_SHARED\OPEN_DECISIONS.md` point 1):** a new space setting «السماح
   للاستقبال بالأسعار اليدوية», **off by default** — a column with a database default `false` for existing
   spaces and the new-space path; this is the schema change of the item (say whether it also joins the
   platform's `newSpaceDefaults`, with your reason). It governs **reception only**: the owner may always type
   a price; **every hand-typed price, by anyone, carries a required reason**. This item stores the setting
   and documents the rule; steps 7 and 8 enforce it. Update `OPEN_DECISIONS.md`'s point 1 as settled (the
   workspace file, in the report, not the repository).
5. **A change applies from then on:** a visit's rates are copied at check-in (the data model already says
   so); the rounding rule and the cap are read at check-out; the capacity and the stay limit apply at once.
   **Here only the documents** (data model, `space-settings`' feature document); steps 7–8 build it.
6. **Audit:** every write is audited with what changed, in the space's audit (conventions §6).
7. **Out:** every web screen (the owner's Settings screen 24 goes to worker A later); the platform settings
   (step 11); the desk's use of any value; announcements; reception's other open decisions (points 2–4).

**Size:** one PR is expected (well under 60 files). If the plan finds otherwise, propose the cut in
"Decisions needed".

## 3. Read first (from `origin/main`)

`CLAUDE.md`; `docs/development/workflow.md`; `docs/development/testing.md`; `docs/backend/conventions.md`
(§6 audit, §7 modules, §8 rules, §9 settings, new-space defaults, occupancy, the front desk);
`docs/api/api-contract.md` (the managed routes, *Spaces (managed)*, *Packages*, *Staff (managed)* as the
latest pattern); `docs/architecture/data-model.md` (*Spaces*, *SpaceSettings*, *Visit charge*);
`docs/backend/security.md` (rate limits, if a write needs one); ADR 0002, 0008, 0009, 0015;
`docs/features/spaces.md` and the feature documents of `space-settings` / `occupancy` if they exist (else
the capability template in `docs/architecture/documentation.md`); `docs/plans/v1-mvp.md` (steps 5, 7, 11 —
this item pulls the space-settings half of step 11 forward: say how the build map records it);
`C:\dev\masaha\workspace\DESIGN\DECISIONS\DECISIONS_OWNER.md` (O2, OW-002, OW-021, OW-024 if it is the
settings screen); `C:\dev\masaha\workspace\_SHARED\OPEN_DECISIONS.md`; the code of `space-settings`,
`platform-settings` (`settingKeys.ts`, the new-space defaults), `spaces` (creation copying the defaults; the
managed routes and their order), `packages` (the latest managed module: routes, `requireCan`, validation,
audit), `shared/auth` (`can.ts`, `requireCan`, `spaceAccess`), `prisma/schema.prisma` (`SpaceSettings`,
`SpaceOccupancy`).

## 4. Findings

New finding numbers start at **94** (in `docs/architecture/findings/`, never GitHub Issues). Record what
the reading finds out of scope; DI-41 is settled in the documents, not recorded.

## 5. Boundaries

`apps/api`, `packages/shared`, `docs`. Nothing in `apps/web`. One schema change (decision 4's column; any
other only with its reason in "Decisions needed"). No dependency. A new error code only if a refusal truly
needs one — then follow `add-error-code`'s rules and say so in "Decisions needed".
