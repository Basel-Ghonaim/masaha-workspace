# ANNOUNCEMENTS — announcements with the closure extension, data reports and favourites, the API (build map step 10) — PLAN ONLY

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

**The task's folder:** `C:\dev\masaha\workspace\WORKER_B\ANNOUNCEMENTS\`. This prompt is `1_PLAN_PROMPT.md`;
**save the plan as `2_PLAN.md` here**; reports `4_REPORT_PR<n>.md`.

**Where you read.** `C:\dev\masaha\app-design` (the read-only worktree reviews and planners use, detached; read
`origin/main` after the fetch — `befd96f9` or later) — commit objects only: `git fetch origin`, then `git show origin/main:<path>`,
`git ls-tree`, `git grep origin/main`. Never check anything out, switch or reset it. Worker B executes
SUBSCRIPTIONS PR 1 in `C:\dev\masaha\app-b` and worker A PUBLIC PR 1a in `C:\dev\masaha\app` — never work
there.

## 0. The base and what runs before it

Plan from today's `origin/main`. Before this item executes, worker B builds, in order: **SUBSCRIPTIONS PRs
1–3** (`C:\dev\masaha\workspace\WORKER_B\SUBSCRIPTIONS\2_PLAN.md` with its approval note — customers;
subscriptions and money; subscription check-ins) and **DEMO_SEED** (`WORKER_B\DEMO_SEED\3_EXEC_PROMPT.md`).
None of them is on `main` yet: plan against what SUBSCRIPTIONS' approved plan says they build (the
subscription's status and progress, `endsOn` moved by an end or an extension, the subscription check-in in
`desk`), and name each assumption you take from it. **This item's executor starts only after all of them have
merged**; its first step is `git diff --name-status <the plan's base> origin/main` and a re-read of the merged
`subscriptions`, `desk` and `customers` code against the plan — a difference the plan does not cover → stop
and ask. Worker A's PUBLIC (`apps/web`, `docs`) runs in parallel: its space-page PR consumes `GET
/spaces/:slug` and `packages/shared`'s `directory` responses, which this item's PR 1 extends — name each shared
code file and document (`docs/features/directory.md`, `api-contract.md`, `v1-mvp.md`, `overview.md`, the
findings index, `docs/README.md`) as a likely text conflict. **Finding numbers:** this item's start at **150**
— write `150`, `151`, … in the plan.

## 1. The plan must stand alone

Fresh Claude Code conversations execute each PR, and another Claude Code conversation reviews each (one
reviewer, no subagents). Every decision with its one-line reason; the files; each route, schema, service
function, transaction and type with its interface; each new error code (through the `add-error-code` skill's
steps, written so an executor without that skill follows them); each test with its lane, title and the break
that must make it fail (`docs/development/testing.md` §3 — **every break run and its red output recorded**);
**each permission (owner, reception, admin, signed-in user, anonymous), each privacy rule (the reporter's
name), each rate limit, each idempotency key and each race gets a deliberate break**; the commits, subjects
counted (≤ 50); fixes before the push folded (`--fixup` + autosquash, `GIT_SEQUENCE_EDITOR=:`); every new
decision and history line ends with its date and `#PRNUM`; the procedure with its commands (branches from the
latest `origin/main` in `C:\dev\masaha\app-b`, `--no-track`; `masaha_b_dev` / `masaha_b_test`; `docker start
masaha-postgres-1`, never `db:up`, never `npm ci`; **memory: one full test run at a time on this machine,
none while a `vitest` of `C:\dev\masaha\app\` runs, the free memory recorded before each full lane; a full
lane killed for low memory is re-run once when the machine is quieter, killed again → carry on and CI's run of
that lane on the pushed head judges (red → stop)**; per commit `lint` + `typecheck`; on the head once
`test:unit`, `test:api`, `format:check`, `check:links`, and `npm run build -w @masaha/shared` if the shared
package changes; **each schema change**: a migration by `migrate dev --create-only` run **once** — then the
executor checks the folder; on data loss Prisma refuses: use `migrate diff --script` — and both B databases
migrated; a real run on 3321 with the demo data (**a demo account or data that does not hold what a real-run
case needs → stop and report; never change data through the app to get past it**); push; `gh pr create
--assignee @me --label feat --label area:api --label area:docs` (`area:web` if the catalogues change); `gh pr
checks` and `CLEAN`; the conflict check); a **"Stop and ask"** list; the executor's stop rule (**a test it
cannot run stops the work** — the same wording as `C:\dev\masaha\workspace\WORKER_B\DESK\3_EXEC_PROMPT_PR3.md`
§2, its break clause included); **never leave silently:** an executor that would leave a carried item or a
review nit undone stops and asks; fix rounds run only what the change touches; the executor's scripts kept in
this folder's `scripts\`, never committed; **carried items:** if a `0_CARRIED_FROM_<n>.md` naming one of these
PRs exists when its executor starts (small fixes from the previous PR's review), its items are that PR's first
commit, named in its description; an appendix mapping steps to Claude's skills, "only a map". Never merge; no
tool attribution; stage by path.

## 2. The owner's decisions (2026-10-21)

**The goal (build map step 10, the API only):** a space tells its users what changes, with the closure
extension; users report wrong information and see the resolution note; users keep their favourite spaces. The
screens (10, 11, 18, 23, 28, and the space page's announcements, report button and heart) are worker A's
later items, planned only once this API has merged. The tables `Announcement`, `ClosureExtension`,
`SubscriptionExtension`, `DataReport`, `Favorite` exist; `announcements` has first reads (`occupancy`
composes them) — read what it holds.

1. **Four PRs in sequence**, each cut from `main` once the one before it has merged:
   - **PR 1 — announcements:** the managed list, create, edit, end now, start now, delete (soft), for the
     owner and reception (ADR 0009); the space's public page (`GET /spaces/:slug`) carries them (decision 6);
     each closure's extension state on the managed list (decision 1); the check-in warning during a closure
     (decision 7).
   - **PR 2 — data reports:** `POST /spaces/:slug/reports` (signed in; the 10-per-hour limit of
     `security.md`, today "not yet built"), `GET /me/reports` (with the resolution note, the reply's author
     as AC-009 words it, `listed: false` for a space that left the directory — C7), the owner's
     `…/data-reports` (verified spaces) and the admin's `/admin/data-reports` (read all; resolve or dismiss
     those of unverified spaces), `can()` with "verified" as its input (conventions › `data-reports`).
   - **PR 3 — favourites:** `GET /me/favorites` (answered whole — C8, its api-contract §4 exception; the
     cards composed by `directory` from `favorites`' ids; `listed: false` — C7), `POST` / `DELETE
     /me/favorites/:spaceId`, idempotent.
   - **PR 4 — the closure extension:** `POST …/announcements/:id/extend-subscriptions`, the owner only, once
     per closure (decisions 2–5).
   If the reading shows a better cut, propose it in *Proposed alternatives* — do not apply it.
2. **The closure's notice to the owner** (`C:\dev\masaha\workspace\_SHARED\OPEN_DECISIONS.md` point 2,
   settled now): reception keeps posting a closure; the owner learns of it **in the app only, no email**: the
   managed announcements list carries each closure's extension state (none yet / applied, with its days and
   how many subscriptions moved), and «يحتاج انتباهك» (the overview, step 12) will count started closures
   without an extension from it — say which read the overview will use; add a route only if none fits. The
   PR's report updates point 2 (the supervisor commits nothing there).
3. **The extension's days:** the server **proposes** the number of Gaza calendar days the closure covers
   (from its start's day to its end's day, or to today when it has no end or has not ended), and the owner
   **types** the number applied, at least one (state a sensible upper bound). Allowed once the closure has
   started (O11), once per closure (the unique key).
4. **Which subscriptions move** (changes a settled line — update `docs/architecture/data-model.md` and
   `docs/project/overview.md` to match, as approved 2026-10-21): every subscription of that space **running on
   any day the closure covered** — it started on or before the closure's last day and ends on or after its
   first — even one that ended during the closure; **excluded:** one ended early (its `endedAt` set) and one
   with no end date. Each moved subscription's `endsOn` moves by the days, a `SubscriptionExtension` row per
   subscription, one transaction under one `Idempotency-Key`; the count in the dialog (O11) is the same rule
   read without writing — say which route answers it. Its status and progress come only from `subscriptions`.
5. **No undo of an extension;** a wrong one is corrected on each subscription (SUBSCRIPTIONS' correction,
   audited).
6. **A closure announcement whose extension was applied:** deleting it, changing its type or its period is
   refused (a `409` with a new code); editing its text stays allowed.
7. **The public page's announcements:** the running and the upcoming ones (not deleted, not ended), ordered
   by start, each with its start and end; ended ones are never public.
8. **A check-in during a running closure** (a visit's or a subscription's) succeeds **with a warning** in
   `meta.warnings`, like `OUTSIDE_OPENING_HOURS` — never refused (say whether it reuses that code or adds one;
   recommend one).
9. **A repeated report** — the same user, space and field while one is open — returns the open report (no new
   row); say its status code and whether it counts toward the hourly limit.
10. **Dismissing a report requires its reply,** for the owner and the admin alike (A8's «لم يُعتمد»); resolving
    keeps the reply optional. The build map's two `data-reports` rows are updated to say so.
11. **A decided report is final:** only an open report is resolved or dismissed; otherwise a `409`.
12. **Favourites have a ceiling** (200), refused with its own code past it, so answering them whole stays
    bounded.

**Unchanged (settled):** announcements are written by the owner and reception, the extension by the owner
only (ADR 0009); an announcement has Arabic text (required), English text (optional), its type and its
period, **no title and no author, no schema change for them** (O9); it can end now, start now, be deleted or
have no end (O10); the reporter is anonymous to the owner («زائر» and the date) and named to the admin (O12)
— the owner's read never carries the name; the owner decides a verified space's reports and the admin an
unverified one's (`security.md`); resolving never edits the space (the «تعديل الحقل» button is navigation);
`listed: false` in favourites and «بلاغاتي» (C7); the report's field groups and «أخرى» with its required
message (the schema's note); the 10-per-hour limit.

## 3. Read first

`CLAUDE.md`; `docs/development/workflow.md`; `testing.md`; `docs/backend/conventions.md` (§4–§9, the
`data-reports` and composed-reads sections, §11, §13); `security.md` (authorization, the rate limits); ADR
0007, 0008, 0009, 0015; `docs/architecture/data-model.md` (the entities, the live state's rules, the
constraints); `docs/api/api-contract.md` (§1–4, the public directory endpoints, *Occupancy (managed)*,
*Front desk (managed)*, the error codes); `docs/features/directory.md`, `occupancy.md`, `desk.md`,
`visits.md`, `space-links.md`, `spaces.md`; `docs/plans/v1-mvp.md` step 10 and the route tables;
`docs/project/overview.md`; the design decisions in `C:\dev\masaha\workspace\DESIGN\DECISIONS\` —
`DECISIONS_OWNER.md` (O9–O12, OW-014), `DECISIONS_ACCOUNT.md` (C6–C8, AC-009, AC-016), `DECISIONS_ADMIN.md`
(A7, A8, AD-012), `DECISIONS_PUBLIC.md` (U8, U10); `_SHARED\OPEN_DECISIONS.md`; SUBSCRIPTIONS' `2_PLAN.md`
(its procedure as the model, and what PRs 1–3 build); the code of `announcements`, `occupancy`, `directory`,
`desk`, `subscriptions`, `space-links`, `users` and `shared/auth` (`can()`, the rate limiter) on
`origin/main`; `schema.prisma` and the migrations that made the five tables; the demo seed; the prototype's
announcements, data-report, favourites and «بلاغاتي» modules (`docs/design/prototype/…`) only where the API's
shape depends on them.

## 4. Decisions the plan must state (with a recommendation each)

- Each route's shape and answer, its bounds (api-contract §4) and pagination; which module owns each route
  (`announcements` L2, `favorites` L2, `data-reports` L3, `subscriptions` for the extension's table, the
  composed reads above them) and that no level rule breaks.
- Gaza time for every "running", "upcoming", "covered day" and "today" (conventions §11).
- The idempotency keys (ADR 0015), the locks, the order of checks and each race: two owners or tabs applying
  one extension; an extension racing an edit of its closure, an end or a correction of a subscription, or a
  renewal; a report decided by the owner and the admin at once as the space's verified state changes; a
  favourite added twice at once.
- The audit lines each write leaves (conventions §6).
- Any migration (indexes for the reads that run, `CHECK`s, the open-report rule of decision 9 if the database
  should hold it), and any document this decision set proves wrong — as a proposal, never applied silently
  (decisions 4 and 10 are already approved).

## 5. The plan's shape

As SUBSCRIPTIONS' `2_PLAN.md`: summary; the contract per PR (scope, acceptance criteria, out of scope); the
reading done and what it changed; the decisions as built; stronger decisions (S…) and **Proposed
alternatives**; related findings (folded or not, why); the files; the interfaces; the tests with their
breaks; the commits; the procedure and the stop rules; the decisions needed from the owner. Stop after saving
it.
